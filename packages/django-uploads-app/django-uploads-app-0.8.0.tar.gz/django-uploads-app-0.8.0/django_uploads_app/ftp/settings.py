import string

from django.conf import settings


all_chars = string.ascii_letters + string.digits
forbidden_chars = ('I', 'l', '1', '|', '0', 'O')

permitted_chars = [el for el in all_chars if el not in forbidden_chars]

PASSWORD_LENGTH = getattr(settings, 'DJANGO_UPLOADS_FTP_PASSWORD_LENGTH', 10)
PASSWORD_CHARS = getattr(settings, 'DJANGO_UPLOADS_FTP_PASSWORD_CHARS', permitted_chars)

# "".join(random.choice(PASSWORD_CHARS) for i in range(PASSWORD_LENGTH))
