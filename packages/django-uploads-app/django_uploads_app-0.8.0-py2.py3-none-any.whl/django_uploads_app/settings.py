import os

from django.conf import settings


USERS_FOLDER = os.path.join(settings.PRIVATE_ROOT, "users")
CURRENT_DIR = os.getcwd()
MINIMUM_FREE_SPACE_MB = getattr(settings, 'DJANGO_UPLOADS_MINIMUM_FREE_SPACE_MB', 1024)
MAX_FILE_SIZE_MB = getattr(settings, 'DJANGO_UPLOADS_MAX_BODY_SIZE_MB', 100)
NGINX_X_ACCEL_REDIRECT = getattr(settings, 'DJANGO_UPLOADS_NGINX_X_ACCEL_REDIRECT', not settings.DEBUG)

DJANGO_UPLOADS_FTP_ENABLED = getattr(settings, 'DJANGO_UPLOADS_FTP_ENABLED', True)
