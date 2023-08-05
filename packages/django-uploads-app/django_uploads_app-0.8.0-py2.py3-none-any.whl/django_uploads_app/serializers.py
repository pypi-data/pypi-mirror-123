from django.template.defaultfilters import linebreaksbr

from rest_framework import serializers
from rest_framework.reverse import reverse


from .models import Link, Upload, FileUpload, UploadType, LinkShare

USER_DETAIL_URL_NAME = 'django_sso_app_user:rest-detail'


class PartialObjectSerializer(serializers.Serializer):
    _partial = serializers.SerializerMethodField(method_name='get_partial')

    def get_partial(self, obj):
        return True


class AbsoluteUrlSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(method_name='get_absolute_url')

    def get_absolute_url(self, obj):
        if getattr(obj, 'pk', None) is not None:
            get_absolute_url = getattr(obj, 'get_relative_url', None)
            if get_absolute_url is None:
                raise NotImplementedError('Model must provide "get_relative_url" method.')
            else:
                request = self.context['request']
                return request.build_absolute_uri(get_absolute_url())


class UserRelatedSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = getattr(obj, 'user', None)
        if user is not None:
            request = self.context['request']
            reverse_url = user.get_relative_rest_url()
            return request.build_absolute_uri(reverse_url)


class DeactivableSerializer(serializers.Serializer):
    is_active = serializers.BooleanField(required=False)


class PublicableSerializer(serializers.Serializer):
    is_public = serializers.BooleanField(required=False)


class TimespanSerializer(serializers.Serializer):
    started_at = serializers.DateTimeField(required=False)
    ended_at = serializers.DateTimeField(required=False)


class UpdatableSerializer(serializers.Serializer):
    updated_at = serializers.DateTimeField(required=False)


class CreatedAtSerializer(serializers.Serializer):
    created_at = serializers.DateTimeField(required=False)


class DownloadLinkField(serializers.Field):
    def get_attribute(self, obj):
        # We pass the object instance onto `to_representation`,
        # not just the field attribute.
        return obj

    def to_representation(self, obj):
        """
        Serialize the download link.
        """
        if getattr(obj, 'secret', None) is not None:
            return reverse('protected_file_download', kwargs={'secret': obj.secret})


class Base64Field(serializers.Field):
    """
    Baes64 field
    """

    def to_representation(self, value):
        return None if value is None else "hidden"

    def to_internal_value(self, data):
        return data if data != '' else None


class PartialLinkSerializer(PartialObjectSerializer,
                            AbsoluteUrlSerializer):
    download_link = serializers.HyperlinkedIdentityField(
        view_name='protected_file_download',
        lookup_field='secret')

    active = serializers.BooleanField()

    def get_absolute_url(self, obj):
        if getattr(obj, 'uuid', None) is not None:
            request = self.context['request']
            return request.build_absolute_uri(reverse('django_uploads:link-detail',
                                                      kwargs={'uuid': obj.uuid}))

    class Meta:
        model = Link
        fields = ('url', 'download_link', 'active', 'is_public', '_partial')
        read_only_fields = ('url', 'uuid', 'download_link', 'active', '_partial')


class PartialFileUploadSerializer(serializers.ModelSerializer):
    upload_url = serializers.CharField(required=False, read_only=True)

    file_path = serializers.SerializerMethodField()

    class Meta:
        model = FileUpload
        fields = ('upload_url', 'file_url', 'uploaded_at', 'file_path')
        read_only_fields = fields

    def get_file_path(self, instance):
        return instance.file_data.name


class UploadTypeSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()

    class Meta:
        model = UploadType
        fields = ('slug', 'name',
                  'is_public',
                  'file_mime',
                  'upload_success_message', 'upload_success_redirect_url',
                  'upload_success_rpc_url',
                  'times_downloadable', 'active_forever', 'active_until',
                  'description',
                  'meta')
        read_only_fields = fields

    def get_description(self, obj):
        """
        Format description field
        """

        if obj.description is not None and obj.description != '':
            return linebreaksbr(obj.description)


class UploadSerializer(AbsoluteUrlSerializer):
    upload_type = serializers.SlugRelatedField(slug_field='slug',
                                               queryset=UploadType.objects.all())

    links = PartialLinkSerializer(many=True, read_only=True)

    get_download_link = serializers.HyperlinkedIdentityField(
        view_name='django_uploads:create-download-link',
        lookup_field='uuid',
        read_only=True)

    comment = serializers.CharField(required=False, allow_null=True,
                                    allow_blank=False)

    slug = serializers.CharField(required=False, allow_null=True,
                                 allow_blank=False)

    file_upload = PartialFileUploadSerializer(required=False, read_only=True)

    file_path = serializers.CharField(required=False, allow_null=True,
                                      allow_blank=False)
    file_base64 = serializers.CharField(required=False, allow_null=True,
                                        allow_blank=False)
    file_url = serializers.CharField(required=False, allow_null=True,
                                     allow_blank=False)
    file_md5 = serializers.CharField(required=False, allow_null=True,
                                     allow_blank=False)
    file_sha1 = serializers.CharField(required=False, allow_null=True,
                                      allow_blank=False)
    file_mime = serializers.CharField(required=False, allow_null=True,
                                      allow_blank=False)

    meta = serializers.CharField(required=False, allow_null=True,
                                 allow_blank=False)

    revision = serializers.CharField(required=False, allow_null=True,
                                     allow_blank=False)

    set_parsed_at = serializers.SerializerMethodField()

    user = serializers.SerializerMethodField()

    def get_user(self, instance):
        request = self.context['request']
        return request.build_absolute_uri(reverse(USER_DETAIL_URL_NAME,
                                                  args=[instance.user.sso_id]))

    def get_absolute_url(self, obj):
        request = self.context['request']
        return request.build_absolute_uri(reverse('django_uploads:upload-detail',
                                                  kwargs={'uuid': obj.uuid}))

    def get_set_parsed_at(self, obj):
        request = self.context['request']
        return request.build_absolute_uri(reverse('django_uploads:set-parsed-at',
                                                  kwargs={'uuid': obj.uuid}))

    def get_set_successfully_parsed(self, obj):
        request = self.context['request']
        return request.build_absolute_uri(reverse('django_uploads:set-successfully-parsed',
                                                  kwargs={'uuid': obj.uuid}))

    def get_set_unsuccessfully_parsed(self, obj):
        request = self.context['request']
        return request.build_absolute_uri(reverse('django_uploads:set-unsuccessfully-parsed',
                                                  kwargs={'uuid': obj.uuid}))

    def validate_upload_type(self, ut):
        if not ut.is_public:
            raise serializers.ValidationError('Upload type is not public')
        return ut

    class Meta:
        model = Upload
        fields = (
            'url', 'uuid', 'created_at', 'updated_at', 'is_active',
            'upload_type',
            'validated_at', 'successfully_validated',
            'parsed_at', 'set_parsed_at', 'successfully_parsed',
            'comment', 'slug', 'revision',
            'file_upload', 'file_url', 'file_name', 'file_url',
            'file_path', 'file_base64', 'file_md5', 'file_sha1', 'file_mime', 'file_size',
            'links', 'get_download_link', 'user',
            'meta')
        read_only_fields = (
            'url', 'uuid', 'created_at', 'updated_at', 'is_active',
            'validated_at', 'successfully_validated',
            'file_upload',
            'file_sha1',
            'links', 'get_download_link', 'user')


class LinkShareSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='resource_type')
    uuid = serializers.CharField(source='resource_uuid')

    class Meta:
        model = Link
        fields = ('type', 'uuid')


class LinkSerializer(AbsoluteUrlSerializer):
    upload = serializers.HyperlinkedRelatedField(many=False,
                                                 view_name='django_uploads:upload-detail',
                                                 read_only=True,
                                                 lookup_field='uuid',
                                                 required=False)

    download_link = serializers.SerializerMethodField()

    active_until = serializers.DateTimeField(required=False, allow_null=True)
    is_public = serializers.BooleanField(required=False, allow_null=False,
                                         default=False)
    times_downloadable = serializers.IntegerField(required=False,
                                                  allow_null=False, default=1)

    shares = LinkShareSerializer(many=True, required=False)

    comment = serializers.CharField(required=False)

    def get_download_link(self, instance):
        if getattr(instance, 'secret', None) is not None:
            request = self.context['request']
            return request.build_absolute_uri(reverse('protected_file_download',
                                                      kwargs={'secret': instance.secret}))

    def get_shares(self, instance):
        return instance.shares.values_list('resource_uuid', flat=True)

    def get_absolute_url(self, obj):
        if getattr(obj, 'uuid', None) is not None:
            request = self.context['request']
            return request.build_absolute_uri(reverse('django_uploads:link-detail',
                                                      kwargs={'uuid': obj.uuid}))

    class Meta:
        model = Link
        fields = (
            'url', 'uuid', 'upload', 'created_at', 'updated_at',
            'active_forever',
            'times_downloadable', 'times_downloaded', 'active_until',
            'download_link', 'downloaded_at', 'is_public', 'shares', 'comment')
        read_only_fields = (
            'uuid', 'upload', 'created_at', 'updated_at', 'download_link',
            'downloaded_at', 'times_downloaded')
