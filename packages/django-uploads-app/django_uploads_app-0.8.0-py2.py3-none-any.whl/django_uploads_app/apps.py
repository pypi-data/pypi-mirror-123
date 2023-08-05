# -*- coding: utf-8
from django.apps import AppConfig


class DjangoUploadsAppConfig(AppConfig):
    name = 'django_uploads_app'

    def ready(self):
        try:
            from . import signals  # noqa F401
            from .ftp import signals

        except ImportError:
            pass
