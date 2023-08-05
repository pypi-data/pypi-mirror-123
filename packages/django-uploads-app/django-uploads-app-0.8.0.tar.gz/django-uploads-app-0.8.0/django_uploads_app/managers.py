from django.db import models


class SlugPKManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class UuidPKManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, uuid):
        return self.get(uuid=uuid)


class UploadManager(UuidPKManager):
    def get_queryset(self):
        return super(UploadManager, self).get_queryset().order_by('-created_at')  # .filter(is_active=True)


class FileUploadManager(UuidPKManager):
    def get_queryset(self):
        return super(FileUploadManager, self).get_queryset().order_by('-created_at')  # .filter(is_active=True)


class LinkManager(UuidPKManager):
    def get_queryset(self):
        return super(LinkManager, self).get_queryset().order_by('-created_at')  # .filter(is_active=True)
