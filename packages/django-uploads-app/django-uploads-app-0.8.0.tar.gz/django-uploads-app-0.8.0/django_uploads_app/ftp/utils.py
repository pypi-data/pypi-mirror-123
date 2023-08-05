import os
import logging
import base64
from subprocess import call

import random
from random import seed

from django.core.management.utils import get_random_secret_key
from django.contrib.auth import get_user_model
from django.conf import settings

from filer.models import File as FilerFile, Folder

from ..utils import get_user_folder_path, get_file_md5sum, get_file_sha1

from .settings import PASSWORD_CHARS, PASSWORD_LENGTH

logger = logging.getLogger('django_uploads_app')

# initializing seed
SEED = int(base64.b16encode(bytes(get_random_secret_key(), 'utf-8')), 16)
seed(SEED)


def get_ftp_user_folder_path(user):
    return os.path.join(get_user_folder_path(user), 'ftp')


def create_user_folder(user):
    user_folder_path = get_ftp_user_folder_path(user)

    try:
        original_umask = os.umask(0)
        os.makedirs(user_folder_path, mode=0o777, exist_ok=True)
    finally:
        os.umask(original_umask)

    return user_folder_path


def create_random_password():
    return "".join(random.choice(PASSWORD_CHARS) for i in range(PASSWORD_LENGTH))


def list_user_files(user):

    user_folders_path = get_ftp_user_folder_path(user)

    user_files = []

    for file_name in os.listdir(user_folders_path):
        file_path = os.path.join(user_folders_path, file_name)
        user_files.append(file_path)

    return user_files


def list_all_users_files():
    all_users_files = {}

    for user in get_user_model().objects.filter(is_superuser=False, is_staff=False, ftp_enabled=True):
        all_users_files[user.sso_id] = list_user_files(user)

    return all_users_files


def parse_user_files(user):
    from ..models import Upload, UploadType

    parsed_files = []

    if not user.ftp_enabled:
        logger.info('Will not parse user files for "{}" because ftp is not enabled'.format(user))
        return parsed_files

    logger.info('Parsing user files for "{}"'.format(user))

    user_files = list_user_files(user)

    for file_path in user_files:
        relative_path = file_path.replace('{}{}'.format(settings.PRIVATE_ROOT, os.path.sep), '')

        file_name = os.path.basename(relative_path)

        existing_upload = Upload.objects.filter(file_path=relative_path).first()

        if existing_upload is None:
            logger.info('Creating upload model for file "{}"'.format(relative_path))

            with open(file_path, 'rb') as fd:
                file_md5sum = get_file_md5sum(fd)
                file_sha1 = get_file_sha1(fd)

            upload_type, _created = UploadType.objects.get_or_create(slug='ftp', name='FTP', is_public=False)

            upload = Upload.objects.create(user=user,
                                           file_name=file_name,
                                           file_path=relative_path,
                                           upload_type=upload_type,
                                           file_md5=file_md5sum,
                                           file_sha1=file_sha1)
            parsed_files.append({
                'path': file_path,
                'relative_path': relative_path,
                'upload': upload.uuid
            })

            # creating filer folders
            existing_filer_file = FilerFile.objects.filter(file=relative_path).first()

            if existing_filer_file is None:
                if os.path.exists(file_path):
                    filer_users_folder, _created = Folder.objects.get_or_create(name='users')
                    filer_user_folder, _created = Folder.objects.get_or_create(name=user.sso_id,
                                                                               parent=filer_users_folder,
                                                                               owner=upload.user)
                    filer_file_folder, _created = Folder.objects.get_or_create(name=upload.upload_type.slug,
                                                                               parent=filer_user_folder)
                    filer_file = FilerFile(original_filename=upload.file_name,
                                           owner=upload.user,
                                           sha1=file_sha1,
                                           folder=filer_file_folder)
                    filer_file.file.name = relative_path

                    setattr(filer_file, '__du__creating', True)
                    filer_file.save()

                    logger.info('Filer file created "{}"'.format(filer_file))

        else:
            logger.info('Upload model already created for file "{}"'.format(relative_path))

    return parsed_files


def parse_all_users_files():
    all_users_parsed_files = {}

    for user in get_user_model().objects.filter(is_superuser=False, is_staff=False):
        all_users_parsed_files[user.sso_id] = parse_user_files(user)

    return all_users_parsed_files


def create_ftp_user(user):
    cmd = 'echo {} | addftpuser -u {}'.format(user.ftp_password, str(user.sso_id))
    exit_code = call(cmd, shell=True)

    return exit_code


def update_ftp_user_password(user):
    cmd = 'echo {} | chpassftpuser -u {}'.format(user.ftp_password, str(user.sso_id))
    exit_code = call(cmd, shell=True)

    return exit_code


def update_ftp_user_quota(user):
    cmd = 'quotaftpset -u {} -q {}'.format(str(user.sso_id), str(user.ftp_quota))
    exit_code = call(cmd, shell=True)

    return exit_code
