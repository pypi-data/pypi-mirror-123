from django.contrib import admin
from django import forms

#from filer.models import ThumbnailOption, FolderPermission
from django_json_widget.widgets import JSONEditorWidget

from .models import UploadType, Upload, FileUpload, Link, LinkShare


class MetaFieldAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MetaFieldAdminForm, self).__init__(*args, **kwargs)
        self.fields['meta'].widget = JSONEditorWidget()


class UploadTypeAdmin(admin.ModelAdmin):
    form = MetaFieldAdminForm
    fields = ('name', 'slug', 'groups',
              'validation_module',
              'is_public',
              'file_mime',
              'upload_success_message', 'upload_success_redirect_url',
              'upload_success_rpc_url',
              'times_downloadable', 'active_forever', 'active_until',
              'description',
              'meta')
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug')


class UploadAdmin(admin.ModelAdmin):
    form = MetaFieldAdminForm
    list_display = ('uuid', 'user', 'upload_type', 'slug', 'revision', 'created_at', 'updated_at', 'is_active')
    search_fields = ('uuid', 'slug', 'rev')


class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'created_at', 'updated_at')


class LinkAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'created_at', 'updated_at', 'is_active')

    def is_active(self, instance):
        return instance.active

    is_active.boolean = True


class LinkShareAdmin(admin.ModelAdmin):
    list_display = ('resource_uuid', 'link', 'created_at')


admin.site.register(UploadType, UploadTypeAdmin)
admin.site.register(Upload, UploadAdmin)
admin.site.register(FileUpload, FileUploadAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(LinkShare, LinkShareAdmin)

# disable filer unwanted features
#admin.site.unregister(ThumbnailOption)
#admin.site.unregister(FolderPermission)
