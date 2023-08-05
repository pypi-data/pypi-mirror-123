import uuid as uuid_lib
import json

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.exceptions import FieldError

from .managers import SlugPKManager, UuidPKManager


class UuidPKModel(models.Model):
    """
    Keeps numeric pk and foreign references by uuid
    """
    objects = UuidPKManager()

    class Meta:
        abstract = True

    # uuid = models.UUIDField(unique=True, db_index=True, default=uuid_lib.uuid4, editable=False)
    uuid = models.CharField(max_length=36, unique=True, db_index=True, default=uuid_lib.uuid4, editable=False)

    def natural_key(self):
        return (self.uuid,)


class SlugPKModel(models.Model):
    objects = SlugPKManager()

    class Meta:
        abstract = True

    name = models.CharField(_("name"), max_length=100)
    slug = models.SlugField(primary_key=True)

    def natural_key(self):
        return (self.slug,)


class DeactivableModel(models.Model):
    class Meta:
        abstract = True

    is_active = models.BooleanField(_('is active'), default=True)


class CreatedAtModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(_('created at'),
                                      editable=False,
                                      auto_now_add=True)


class UpdatableModel(models.Model):
    class Meta:
        abstract = True

    updated_at = models.DateTimeField(_('updated at'),
                                      editable=False,
                                      null=True,
                                      blank=True)

    def save(self, *args, **kwargs):
        if not self._state.adding:
            self.updated_at = timezone.now()
        return super(UpdatableModel, self).save(*args, **kwargs)


class UserRelatedModel(models.Model):
    class Meta:
        abstract = True

    #user = models.ForeignKey(User, on_delete=models.CASCADE,
    #                         verbose_name=_('user'))


class PublicableModel(models.Model):
    class Meta:
        abstract = True

    is_public = models.BooleanField(_('is public'), default=False)


class TimespanModel(models.Model):
    class Meta:
        abstract = True

    started_at = models.DateTimeField(_('started at'), null=True, blank=True)

    ended_at = models.DateTimeField(_('ended at'), null=True, blank=True)


class MetaFieldModel(models.Model):
    class Meta:
        abstract = True

    meta = models.TextField(verbose_name=_('Meta'),
                            null=True,
                            blank=True)

    def save(self, *args, **kwargs):
        if self.meta is not None and self.meta.strip() in ('', '{}', 'None'):
            self.meta = None
        else:
            if self.meta is not None:
                try:
                    json.loads(self.meta)
                except ValueError:
                    raise FieldError('Invalid JSON on meta field')

        return super(MetaFieldModel, self).save(*args, **kwargs)
