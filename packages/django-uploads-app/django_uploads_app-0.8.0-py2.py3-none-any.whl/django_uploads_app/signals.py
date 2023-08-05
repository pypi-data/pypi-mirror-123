import os
import logging

from django.db.models.signals import pre_delete, post_delete, pre_save, post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model

from filer.models import File, Image, Folder

from django_sso_app.core.apps.profiles.models import Profile

from .utils import delete_file, get_file_md5sum, get_file_sha1, get_file_mimetype, create_user_folder
from .models import FileUpload, Upload, UploadType

logger = logging.getLogger('django_uploads_app')
User = get_user_model()


@receiver(post_save, sender=Profile)
def _create_user_uploads_folder(sender, instance, created, **kwargs):
    """
    Creates user private files folder in fs and virtual filer folders
    """
    # if kwargs['raw']:
    #     # https://github.com/django/django/commit/18a2fb19074ce6789639b62710c279a711dabf97
    #     return

    user = instance.user

    if created and not user.is_superuser:
        logger.info('user {} created, creating user folder'.format(user))
        create_user_folder(user)

        logger.info('user {} created, creating user filer folders'.format(user))
        user.create_filer_folders()


@receiver(user_logged_in)
def _create_user_uploads_folder_for_legacy_users(**kwargs):
    """
    Enforce post login user folder creation, noqa.
    """
    user = kwargs['user']

    if not user.is_superuser:
        logger.info('user {} logged in, try creating user folder'.format(user))
        create_user_folder(user)

        logger.info('user {} logged in, try creating user filer folders'.format(user))
        user.create_filer_folders()


@receiver(pre_delete, sender=FileUpload)
def _bind_file_data_path_and_filer_file_to_deleting_instance(sender, instance, **kwargs):
    """ Save file path references for `post_delete` signal """
    if instance.file_data:
        setattr(instance, '__du__file_data', instance.file_data.path)
    if instance.filer_file is not None:
        setattr(instance, '__du__filer_file', instance.filer_file)


@receiver(post_delete, sender=FileUpload)
def _delete_file_data_on_model_deletion(sender, instance, **kwargs):
    """ Deletes image files and filer_file on `post_delete` """
    file_data_path = getattr(instance, '__du__file_data', None)
    if file_data_path is not None:
        logger.info('Deleting file_data {}'.format(file_data_path))
        delete_file(file_data_path)

    filer_file = getattr(instance, '__du__filer_file', None)
    if filer_file is not None:
        filer_file.delete()


@receiver(pre_save, sender=FileUpload)
def _create_filer_file_before_upload(sender, instance, **kwargs):
    """
    Creates filer file for FileUpload instances with file_data
    """
    if kwargs['raw']:
        # https://github.com/django/django/commit/18a2fb19074ce6789639b62710c279a711dabf97
        return

    if bool(instance.file_data) and not bool(instance.filer_file):
        setattr(instance, '__du__creating_filer_file', True)

        filer_file = File.objects.create(original_filename=instance.upload.file_name,
                                         owner=instance.upload.user,
                                         sha1=instance.upload.file_sha1)

        setattr(filer_file, '__du__creating', True)

        instance.filer_file = filer_file


@receiver(post_save, sender=FileUpload)
def _update_filer_file_after_upload(sender, instance, created, **kwargs):
    """
    Updates filer file model
    """
    if kwargs['raw']:
        # https://github.com/django/django/commit/18a2fb19074ce6789639b62710c279a711dabf97
        return

    if getattr(instance, '__du__creating_filer_file', False):
        file_path = instance.file_data.path

        logger.info('Creating filer file for path "{}"'.format(file_path))

        instance.filer_file.file = instance.file_data
        filer_users_folder, _created = Folder.objects.get_or_create(name='users')
        filer_user_folder, _created = Folder.objects.get_or_create(name=instance.upload.user.sso_id,
                                                                   parent=filer_users_folder,
                                                                   owner=instance.upload.user,)
        instance.filer_file.folder, _created = Folder.objects.get_or_create(name=instance.upload.upload_type.slug,
                                                                            parent=filer_user_folder)

        setattr(instance.filer_file, '__du__creating', True)

        instance.filer_file.save()


@receiver(pre_save)
def _set_right_filer_file_owner(sender, instance, **kwargs):
    if kwargs['raw']:
        # https://github.com/django/django/commit/18a2fb19074ce6789639b62710c279a711dabf97
        return

    if sender in [File, Image]:
        if bool(instance.file) and not getattr(instance, '__du__creating', False):
            logger.info('Setting file owner for "{}"'.format(instance))

            file_owner = getattr(instance, 'owner', None)
            file_folder = getattr(instance, 'folder', None)

            if file_folder is not None:
                folder_owner = getattr(file_folder, 'owner')

                if file_owner != folder_owner:
                    logger.info('Setting file owner for "{}" to "{}"'.format(instance, folder_owner))
                    instance.owner = folder_owner


@receiver(post_save)
def _create_upload_object_for_filer_file(sender, instance, created, **kwargs):
    """
    When file is uploaded from django admin, creates a new upload object with file_path
    """
    if kwargs['raw']:
        # https://github.com/django/django/commit/18a2fb19074ce6789639b62710c279a711dabf97
        return

    if sender in [File, Image]:
        if bool(instance.file) and not getattr(instance, '__du__creating', False):
            file_owner = getattr(instance, 'owner', None)
            file_folder = getattr(instance, 'folder', None)

            if file_folder is not None:
                file_owner = getattr(file_folder, 'owner')
                upload_type_slug = file_folder.name
            else:
                upload_type_slug = 'file'

            file_path = instance.file.path.replace(str(settings.PRIVATE_ROOT), '').lstrip(os.path.sep)
            logger.info('Django admin uploaded filer file_path "{}"'.format(file_path))

            new_upload = Upload.objects.create(
                user=file_owner,
                upload_type=UploadType.objects.get(slug=upload_type_slug),
                file_name=instance.name,
                file_path=file_path,
                file_size=instance.file.size,
                file_sha1=get_file_sha1(instance.file),
                file_md5=get_file_md5sum(instance.file),
                file_mime=get_file_mimetype(instance.file.path)[0]
            )

            logger.info('Upload object created for filer file "{}"'.format(new_upload))


@receiver(post_delete)
def _update_upload_object_for_filer_deleted_file(sender, instance, **kwargs):
    """
    When filer file is deleted from django admin its upload object should persist with updated file_path property
    """
    if sender in [File, Image]:
        file_path = instance.file.path.replace(str(settings.PRIVATE_ROOT), '').lstrip(os.path.sep)
        deleted_file_uploads = Upload.objects.filter(file_path=file_path)

        if len(deleted_file_uploads) > 0:
            deleted_file_upload_object = deleted_file_uploads[0]

            deleted_file_upload_object.file_path = '{}.deleted'.format(file_path)
            deleted_file_upload_object.save()

            logger.info('Upload object updated for deleted filer file "{}"'.format(deleted_file_upload_object))
