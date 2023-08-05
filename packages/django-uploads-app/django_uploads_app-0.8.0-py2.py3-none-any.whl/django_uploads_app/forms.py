import logging

import json

from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import FileUpload, Link
from .utils import get_file_md5sum, get_file_sha1

logger = logging.getLogger('apps.uploads')


def validate_uploaded_file(upload, file_data):
    # validating by validation_module function

    validation_function = upload.get_validation_function()

    if validation_function is None:
        logger.info('Upload has no validation_function, setting as successfully validated.')
        upload.validated_at = timezone.now()
        upload.successfully_validated = True
        upload.save()

    else:
        file_path = 'file://' + file_data.file.name

        validation_kwargs = {}

        uploadtype_meta = upload.upload_type.meta
        if uploadtype_meta is not None and uploadtype_meta != '':
            ut_meta = json.loads(uploadtype_meta)

            if ut_meta.get('options', None) is not None:
                upload_meta = json.loads(upload.meta)
                validation_kwargs['options'] = upload_meta['options']

        logger.info('Validating file {}'.format(file_path))

        valid, _err = validation_function(file_path, **validation_kwargs)

        upload.validated_at = timezone.now()

        if valid:
            upload.successfully_validated = True
            upload.save()
        else:
            upload.successfully_validated = False
            upload.save()
            raise ValidationError(_err)


class FileUploadForm(forms.ModelForm):
    file_data = forms.FileField(
        label='Select a file',
        help_text='max. 300 megabytes'
    )

    get_upload_link = forms.BooleanField(initial=False, required=False)
    active_forever = forms.BooleanField(initial=False, required=False)
    active_until = forms.DateTimeField(required=False)
    times_downloadable = forms.IntegerField(required=False, min_value=0, initial=1)
    public = forms.BooleanField(initial=False, required=False)

    def __init__(self, *args, **kwargs):
        # important to "pop" added kwarg before call to parent's constructor
        self.request = kwargs.pop('request')
        self.file_upload = kwargs.pop('file_upload')

        super(FileUploadForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        upload = self.file_upload.upload
        file_data = cleaned_data.get('file_data')

        uploaded_file_md5_sum = get_file_md5sum(file_data)
        uploaded_file_sha1 = get_file_sha1(file_data)

        validate_uploaded_file(upload, file_data)

        # validating uploaded_file_md5_sum
        if upload.file_md5 is not None:
            logger.debug('md5: {}'.format(uploaded_file_md5_sum))
            if uploaded_file_md5_sum != upload.file_md5:
                raise ValidationError('MD5SUM mismatch.')
        else:
            upload.file_md5 = uploaded_file_md5_sum

        received_content_type = file_data.content_type
        file_size = file_data.size

        if upload.file_size == 0:
            upload.file_size = file_size

        if upload.file_mime is None:
            upload.file_mime = received_content_type

        # saving generated sha1
        upload.file_sha1 = uploaded_file_sha1

        self.file_upload.file_data = file_data
        self.file_upload.uploaded_at = timezone.now()

    def save(self, **kwargs):
        data = self.cleaned_data

        self.file_upload.save()
        self.file_upload.upload.save()

        if data.get('get_upload_link', False):
            logger.info('Creating download link for "{}" because of {}'.format(self.file_upload.upload, data))

            active_until = data.get('active_until', None)
            active_forever = data.get('active_forever', False)
            is_public = data.get('public', False)
            times_downloadable = 0 if active_forever else data.get('times_downloadable', 1)

            link = Link.objects.create(upload=self.file_upload.upload,
                                       active_forever=active_forever,
                                       active_until=active_until,
                                       times_downloadable=times_downloadable,
                                       is_public=is_public)

            logger.info('Download link created "{}"'.format(link))

        return self.file_upload

    class Meta:
        model = FileUpload
        fields = ('file_data',)
