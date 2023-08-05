from django_filters import rest_framework as filters

from .models import Upload, UploadType


class UploadFilter(filters.FilterSet):
    upload_type = filters.ModelChoiceFilter(to_field_name='slug', queryset=UploadType.objects.all())

    class Meta:
        model = Upload
        fields = {
            'upload_type': ['exact'],
            'slug': ['exact'],
            'revision': ['exact'],
            'user__sso_app_profile__sso_id': ['exact'],
            'created_at': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'updated_at': ['exact', 'gt', 'lt', 'gte', 'lte', 'isnull'],
            'validated_at': ['exact', 'gt', 'lt', 'gte', 'lte', 'isnull'],
            'successfully_validated': ['exact', 'isnull'],
            'parsed_at': ['exact', 'gt', 'lt', 'gte', 'lte', 'isnull'],
            'successfully_parsed': ['exact', 'isnull'],
        }
