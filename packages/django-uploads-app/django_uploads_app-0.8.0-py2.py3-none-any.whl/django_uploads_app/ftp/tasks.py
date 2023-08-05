from __future__ import absolute_import

from django.contrib.auth import get_user_model

from celery import shared_task
from celery.utils.log import get_task_logger

# tasks
# celery conf

from ..utils import run_task
from .utils import list_user_files as _list_user_files
from .utils import list_all_users_files as _list_all_users_files
from .utils import parse_user_files as _parse_user_files
from .utils import parse_all_users_files as _parse_all_users_files

MODULE_NAME = 'apps.ftp'


@shared_task(bind=True)
def list_user_files(self, user_sso_id, **kwargs):
    _logger = get_task_logger('{}.{}'.format(MODULE_NAME, 'list_user_files'))

    kwargs['user'] = get_user_model().objects.get(sso_app_profile__sso_id=user_sso_id)

    return run_task(_list_user_files, _logger, **kwargs)


@shared_task(bind=True)
def list_all_users_files(self, **kwargs):
    _logger = get_task_logger('{}.{}'.format(MODULE_NAME, 'list_all_users_files'))

    return run_task(_list_all_users_files, _logger, **kwargs)


@shared_task(bind=True, soft_time_limit=300, time_limit=300)
def parse_user_files(self, user_sso_id, **kwargs):
    _logger = get_task_logger('{}.{}'.format(MODULE_NAME, 'parse_user_files'))

    kwargs['user'] = get_user_model().objects.get(sso_app_profile__sso_id=user_sso_id)

    return run_task(_parse_user_files, _logger, **kwargs)


@shared_task(bind=True, soft_time_limit=600, time_limit=600)
def parse_all_users_files(self, **kwargs):
    _logger = get_task_logger('{}.{}'.format(MODULE_NAME, 'parse_all_users_files'))

    return run_task(_parse_all_users_files, _logger, **kwargs)
