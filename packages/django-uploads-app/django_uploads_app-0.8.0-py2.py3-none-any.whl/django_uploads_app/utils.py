import os
import hashlib
from functools import partial
import uuid as uuid_lib
from subprocess import call
import platform

from mimetypes import MimeTypes

from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings

# from pytz import utc
from pytz import timezone as pytz_timezone

from .settings import USERS_FOLDER

TZ = pytz_timezone('utc')
mime = MimeTypes()


if platform.system() == 'Windows':
    def local_space_available(dir):
        """Return space available on local filesystem."""
        import ctypes
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dir), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value
else:
    def local_space_available(dir):
        destination_stats = os.statvfs(dir)
        return destination_stats.f_bsize * destination_stats.f_bavail


def run_task(f, logger, **kwargs):
    errors = []
    result = None

    try:
        result = f(**kwargs)

    except Exception as e:
        if hasattr(e, 'message'):
            msg = e.message
        else:
            msg = str(e)

        print('Task failed "{}"'.format(msg))
        logger.exception(msg)
        errors.append(msg)

    ret = {
        'data': {
            'result': result
        },
        'meta': {
            'status': 'OK' if len(errors) == 0 else 'ERROR',
            'errors': {}
        }
    }
    ret['meta']['errors'] = errors

    return ret


def get_file_md5sum(file, block_size=65536):
    hasher = hashlib.md5()

    file.seek(0)
    for buf in iter(partial(file.read, block_size), b''):
        hasher.update(buf)

    md5 = hasher.hexdigest()
    # to make sure later operations can read the whole file
    file.seek(0)

    return md5


def get_file_sha1(file):
    hasher = hashlib.sha1()

    file.seek(0)
    while True:
        buf = file.read(104857600)
        if not buf:
            break
        hasher.update(buf)

    sha1 = hasher.hexdigest()
    # to make sure later operations can read the whole file
    file.seek(0)

    return sha1


def get_file_mimetype(file_path):
    return mime.guess_type(file_path)


def get_new_uuid():
    return str(uuid_lib.uuid4())


def create_secret():
    now = str(timezone.now())
    key = "{}{}{}".format(now, settings.SECRET_KEY, get_new_uuid()).encode('utf-8')

    return hashlib.sha224(key).hexdigest()


def delete_file(path):
   """
   Deletes file path from filesystem.
   """
   if os.path.isfile(path):
       os.remove(path)


def get_user_folder_path(user):
    return os.path.join(USERS_FOLDER, str(user.sso_id))


def run_script(script_path, *args):
    cmd = script_path + ' ' + ' '.join(args)
    print('Running "{}"'.format(cmd))

    exit_code = call(cmd, shell=True)

    return exit_code


def get_nginx_file_response(file_path):
    response = HttpResponse()

    response['X-Accel-Redirect'] = file_path
    response['Content-Type'] = ''  # https://serverfault.com/questions/195060/nginx-x-accel-redirect-and-mime-types
    response['Cache-Control'] = 'public, must-revalidate'
    response['Pragma'] = 'no-cache'

    return response


def get_uploads_user_folder_path(user):
    return os.path.join(get_user_folder_path(user), 'file')


def create_user_folder(user):
    user_folder_path = get_uploads_user_folder_path(user)

    try:
        original_umask = os.umask(0)
        os.makedirs(user_folder_path, mode=0o777, exist_ok=True)
    finally:
        os.umask(original_umask)

    return user_folder_path


def get_filer_file_absolute_path(filer_file):
    if getattr(filer_file, 'folder', None) is not None:
        folder = filer_file.folder

        folders = [folder.name]

        while folder.parent is not None:
            folders.append(folder.parent.name)
            folder = folder.parent

        return os.path.sep.join(reversed(folders))

    else:
        # Unsorted Uploads
        return ''


def generate_filer_filename(instance, filename):
    # instance file will be uploaded to PRIVATE_ROOT/users/<user__sso_id>/<upload_type__slug>/<filename>

    file_path = get_filer_file_absolute_path(instance)

    return os.path.join(file_path, filename)
