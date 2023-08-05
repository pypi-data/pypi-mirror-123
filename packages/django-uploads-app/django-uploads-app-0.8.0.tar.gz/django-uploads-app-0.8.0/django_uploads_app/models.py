import logging

from importlib import import_module
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models
from django.db import transaction
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from rest_framework.reverse import reverse

from filer.fields.file import FilerFileField

from .permissions import is_staff
from .base_models import CreatedAtModel, UpdatableModel, UuidPKModel, PublicableModel, SlugPKModel, MetaFieldModel
from .utils import get_new_uuid, create_secret
from .storage import custom_fs

from .managers import LinkManager, UploadManager, FileUploadManager

logger = logging.getLogger('django_uploads_app')
User = get_user_model()


def get_uploaded_file_path(instance, filename):
    # file will be uploaded to PRIVATE_ROOT/users/<user__sso_id>/<upload__upload_type/<filename>
    return 'users/{0}/{1}/{2}'.format(instance.upload.user.sso_id,
                                      instance.upload.upload_type.slug,
                                      filename)


class UploadType(SlugPKModel, PublicableModel, MetaFieldModel):
    groups = models.ManyToManyField(Group, verbose_name=_('Groups'),
                                    blank=True)

    validation_module = models.CharField(verbose_name=_('Validation module'),
                                         max_length=255,
                                         null=True,
                                         blank=True)

    file_mime = models.CharField(verbose_name=_('File mime'),
                                 max_length=255,
                                 null=True,
                                 blank=True)

    upload_success_message = models.TextField(
        verbose_name=_('Upload success message'),
        null=True,
        blank=True)

    upload_success_redirect_url = models.TextField(
        verbose_name=_('Upload success redirect URL'),
        null=True,
        blank=True)

    upload_success_rpc_url = models.TextField(
        verbose_name=_('Upload success RPC URL'),
        null=True,
        blank=True)

    times_downloadable = models.PositiveIntegerField(
        verbose_name=_('Times downloadable'),
        null=True,
        blank=True)

    active_forever = models.BooleanField(verbose_name=_('Active forever'),
                                         default=True)

    active_until = models.DateTimeField(verbose_name=_('Active until'),
                                        null=True,
                                        blank=True)

    description = models.TextField(
        verbose_name=_('Description'),
        null=True,
        blank=True)

    @classmethod
    def get_user_upload_types(cls, user):
        return cls.objects.filter(groups__isnull=True) | cls.objects.filter(
            groups__in=user.groups.all())

    def __str__(self):
        return self.name


class Upload(UuidPKModel, CreatedAtModel, UpdatableModel, MetaFieldModel):
    user = models.ForeignKey(User, verbose_name=_('User'),
                             related_name='uploads', db_index=True, on_delete=models.CASCADE)

    upload_type = models.ForeignKey(UploadType, verbose_name=_('upload type'), on_delete=models.CASCADE)

    comment = models.TextField(verbose_name=_('Comment'),
                               null=True,
                               blank=True)

    slug = models.SlugField(verbose_name=_('Slug'),
                            max_length=255,
                            null=True,
                            blank=True,
                            db_index=True)

    is_active = models.BooleanField(verbose_name=_('Is active'),
                                    default=True)

    file_name = models.CharField(verbose_name=_('File name'),
                                 max_length=512)

    file_base64 = models.TextField(verbose_name=_('File base64'),
                                   null=True,
                                   blank=True)

    file_url = models.CharField(verbose_name=_('File url'),
                                max_length=2048,
                                null=True,
                                blank=True)

    file_path = models.CharField(verbose_name=_('File path'),
                                 max_length=2048,
                                 null=True,
                                 blank=True,
                                 db_index=True)

    file_md5 = models.CharField(verbose_name=_('File md5'),
                                max_length=32,
                                null=True,
                                blank=True)

    file_sha1 = models.CharField(verbose_name=_('File sha1'),
                                 max_length=40,
                                 null=True,
                                 blank=True)

    file_mime = models.CharField(verbose_name=_('File mime'),
                                 max_length=255,
                                 null=True,
                                 blank=True)

    file_size = models.PositiveIntegerField(verbose_name=_('File size'),
                                            default=0)

    validated_at = models.DateTimeField(verbose_name=_('Validated at'), null=True, blank=True)
    successfully_validated = models.NullBooleanField(verbose_name=_('Successfully validated'), null=True, blank=True)

    parsed_at = models.DateTimeField(verbose_name=_('Parsed at'), null=True, blank=True)
    successfully_parsed = models.NullBooleanField(verbose_name=_('Successfully parsed'), null=True, blank=True)

    revision = models.CharField(verbose_name='Revision', max_length=255, null=True, blank=True)

    objects = UploadManager()

    def has_file(self):
        return (self.file_url is not None and
                self.file_base_64 is not None and
                self.file_path is not None and
                (not hasattr(self, 'file_upload') or (
                        hasattr(self, 'file_uploaded') and
                        self.file_uploaded.uploaded_at is not None)))

    def create_file_upload(self, request=None, uploaded_at=None, upload_url=None):
        if getattr(self, 'file_upload', None) is not None:
            return self.file_upload
        else:
            logger.info('Creating FileUpload instance')
            file_upload_uuid = get_new_uuid()

            if upload_url is None:
                if request is not None:
                    upload_url = request.build_absolute_uri(reverse('django_uploads:file-upload',
                                                            kwargs={'uuid': file_upload_uuid}))
                else:
                    from django.contrib.sites.models import Site
                    from django.conf import settings

                    current_site = Site.objects.get(pk=settings.SITE_ID)
                    upload_url = settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL + '://' + \
                                 current_site.domain + reverse('django_uploads:file-upload',
                                                               kwargs={'uuid': file_upload_uuid})

            file_upload = FileUpload.objects.create(
                uuid=file_upload_uuid,
                upload=self,
                upload_url=upload_url,
                uploaded_at=uploaded_at
            )

            logger.info('Created FileUpload instance: {}'.format(file_upload))

            return file_upload

    def create_download_link(self, active_forever=False, times_downloadable=1, is_public=False, active_until=None,
                             comment=None,
                             shares=[]):
        if is_public == 'true':
            is_public = True
        if active_forever == 'true':
            active_forever = True

        with transaction.atomic():
            link = Link.objects.create(
                upload=self,
                active_until=active_until,
                active_forever=active_forever,
                times_downloadable=times_downloadable,
                comment=comment,
                is_public=is_public)

            logger.info('Created download link {}'.format(link))

            for s in shares:
                resource_type, resource_uuid = s.split(':')
                LinkShare.objects.create(link=link, resource_type=resource_type, resource_uuid=resource_uuid)

            return link

    def get_validation_function(self):
        """
        Returns validation module function
        """
        validation_module_name = self.upload_type.validation_module

        if validation_module_name is not None and validation_module_name != '':
            module = import_module(validation_module_name)

            return module.validate

    def __str__(self):
        return '{}:{}'.format(self.__class__.__name__, self.uuid)


class FileUpload(UuidPKModel, CreatedAtModel, UpdatableModel):
    upload = models.OneToOneField(Upload, verbose_name=_('Upload'),
                                  related_name='file_upload',
                                  on_delete=models.CASCADE)

    upload_url = models.CharField(verbose_name=_('Upload url'),
                                  max_length=255)

    file_url = models.CharField(verbose_name=_('File url'),
                                max_length=2048,
                                null=True,
                                blank=True)

    uploaded_at = models.DateTimeField(_('date uploaded'),
                                       null=True,
                                       blank=True)

    file_data = models.FileField(storage=custom_fs,
                                 upload_to=get_uploaded_file_path,
                                 null=True,
                                 blank=True)

    filer_file = FilerFileField(null=True,
                                blank=True,
                                on_delete=models.SET_NULL)

    objects = FileUploadManager()

    def __str__(self):
        return '{}:{}'.format(self.__class__.__name__, self.uuid)


class Link(UuidPKModel, CreatedAtModel, UpdatableModel):
    upload = models.ForeignKey(Upload, verbose_name=_('Upload'),
                               related_name='links', on_delete=models.CASCADE)

    secret = models.CharField(verbose_name=_('Secret'),
                              max_length=2048, unique=True,
                              default=create_secret,
                              db_index=True)

    comment = models.TextField(verbose_name=_('Comment'),
                               null=True,
                               blank=True)

    downloaded_at = models.DateTimeField(verbose_name=_('Last download'),
                                         null=True,
                                         blank=True)

    times_downloadable = models.PositiveIntegerField(
        verbose_name=_('Times downloadable'),
        null=True,
        blank=True)

    times_downloaded = models.PositiveIntegerField(
        verbose_name=_('Times downloaded'),
        default=0)

    active_forever = models.BooleanField(verbose_name=_('Active forever'),
                                         default=True)

    active_until = models.DateTimeField(verbose_name=_('Active until'),
                                        null=True,
                                        blank=True)

    is_public = models.BooleanField(verbose_name=_('Is public'),
                                    default=False)

    objects = LinkManager()

    @property
    def last_download(self):
        return self.downloaded_at

    @property
    def active(self):
        # print('active_forever', self.active_forever)
        # print('available', self.times_downloadable)
        # print('downloaded', self.times_downloaded)
        # print('until', self.active_until)

        if self.active_forever:
            return True

        if self.times_downloadable is not None:
            if (self.times_downloadable - self.times_downloaded) > 0:
                return True

        if self.active_until is not None:
            if (self.active_until - timezone.now()).seconds > 0:
                return True

        return False

    def is_available_for_user(self, user):
        if self.active:
            if self.is_public:
                return True

            if self.upload.user == user:
                return True

            if is_staff(user):
                return True

        if user.is_anonymous:
            return False
        else:
            group_link_shares = self.shares.filter(resource_type='group').values_list('resource_uuid',
                                                                                      flat=True)

            sharing_groups_count = user.groups.filter(
                name__in=group_link_shares).count()

            user_link_shares_count = self.shares.filter(resource_type='user',
                                                        resource_uuid=user.sso_id).count()

            available_shares_count = user_link_shares_count + sharing_groups_count

            return (available_shares_count > 0) and self.active

    def __str__(self):
        return '{}:{}'.format(self.__class__.__name__, self.uuid)


class LinkShare(UuidPKModel, CreatedAtModel, UpdatableModel):
    RESOURCE_TYPE_CHOICES = (
        ('user', 'User'),
        ('group', 'Group')
    )

    permissions = models.CharField(_('permissions'), max_length=10, null=True, blank=True)

    link = models.ForeignKey(Link, verbose_name=_('Link'),
                             related_name='shares', on_delete=models.CASCADE)

    resource_type = models.CharField(verbose_name=_('Resource type'),
                                     choices=RESOURCE_TYPE_CHOICES,
                                     null=True,
                                     blank=True,
                                     max_length=255)

    resource_uuid = models.CharField(verbose_name=_('Resource UUID'),
                                     null=True,
                                     blank=True,
                                     max_length=255)

    def __str__(self):
        return self.resource_type + ':' + self.resource_uuid
