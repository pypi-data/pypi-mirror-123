from django.apps import AppConfig


class FtpConfig(AppConfig):
    name = 'apps.ftp'

    def ready(self):
        try:
            from . import signals  # noqa F401
            from .models import UploadType

            _ftp_upload_type, _created = UploadType.objects.get_or_create(name='FTP', slug='ftp', is_public=False)

        except ImportError:
            pass
