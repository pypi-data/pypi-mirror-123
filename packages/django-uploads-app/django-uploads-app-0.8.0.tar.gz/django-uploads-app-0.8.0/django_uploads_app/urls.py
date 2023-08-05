from django.conf.urls import url
from django.views.generic import TemplateView
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'django_uploads'

_urlpatterns = [
    url(r'^upload-types/$', views.UploadTypeViewSet.as_view({'get': 'list'}),
        name="upload-type-list"),

    url(r'^uploads/$',
        views.UploadViewSet.as_view({'get': 'list', 'post': 'create'}),
        name="upload-list"),
    url(r'^uploads/(?P<uuid>[0-9a-f-]+)/$',
        views.UploadViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}),
        name="upload-detail"),
    url(r'^uploads/(?P<uuid>[0-9a-f-]+)/create_download_link/$',
        views.CreateDownloadLink.as_view(), name='create-download-link'),

    url(r'^uploads/(?P<uuid>[0-9a-f-]+)/set-parsed/$',
        views.SetUploadParsedAt.as_view(), name='set-parsed-at'),
    url(r'^uploads/(?P<uuid>[0-9a-f-]+)/set-successfully-parsed/$',
        views.SetUploadSuccessfullyParsed.as_view(), name='set-successfully-parsed'),
    url(r'^uploads/(?P<uuid>[0-9a-f-]+)/set-unsuccessfully-parsed/$',
        views.SetUploadUnsuccessfullyParsed.as_view(), name='set-unsuccessfully-parsed'),

    url(r'^file-upload/(?P<uuid>[0-9a-f-]+)/$', views.FileUploadView.as_view(),
        name='file-upload'),
    url(r'^file-upload/success/$',
        TemplateView.as_view(template_name="uploads/file_upload_success.html"),
        name='file-upload-success'),

    # url(r'^links/$', views.LinkViewSet.as_view({'get': 'list'}),
    # name="link-list"),
    url(r'^links/(?P<uuid>[0-9a-f-]+)/$', views.LinkViewSet.as_view(
        {'get': 'retrieve', 'delete': 'destroy', 'patch': 'partial_update'}),
        name="link-detail"),

]

download_link_urlpattern = url(r'^links/(?P<secret>\w+)/$',
                               views.GetProtectedFileView.as_view(),
                               name='protected_file_download')

api_urlpatterns = (format_suffix_patterns(_urlpatterns), app_name)
