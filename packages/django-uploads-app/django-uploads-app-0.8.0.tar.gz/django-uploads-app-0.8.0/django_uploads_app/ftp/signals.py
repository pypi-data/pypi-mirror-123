import logging

from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from django_sso_app.core.apps.profiles.models import Profile

from .utils import create_user_folder, create_ftp_user, update_ftp_user_password, update_ftp_user_quota

logger = logging.getLogger('django_uploads_app')
User = get_user_model()


@receiver(post_save, sender=Profile)
def _create_user_proftpd_config(sender, instance, created, **kwargs):
    # if kwargs['raw']:
    #     # https://github.com/django/django/commit/18a2fb19074ce6789639b62710c279a711dabf97
    #     return

    user = instance.user

    if created and not user.is_superuser and user.ftp_enabled:
        if created:
            logger.info('user created, creating user folder and proftpd config')
            create_user_folder(user)

            logger.info('user created, creating proftpd user config')
            exit_code = create_ftp_user(user)
            logger.info('Exit code: {}'.format(exit_code))

            logger.info('user created, updating proftpd quota')
            exit_code_2 = update_ftp_user_quota(user)
            logger.info('Exit code: {}'.format(exit_code_2))


@receiver(user_logged_in)
def _create_user_proftpd_config_for_legacy_users(**kwargs):
    """
    Enforce post login user proftpd config creation, noqa.
    """
    user = kwargs['user']

    if not user.is_superuser and user.ftp_enabled:
        logger.info('user {} logged in, try creating user folder and proftpd config'.format(user))
        create_user_folder(user)

        logger.info('user logged in, try creating proftpd user config')
        exit_code = create_ftp_user(user)
        logger.info('Exit code: {}'.format(exit_code))

        logger.info('user logged in, try updating proftpd quota')
        exit_code_2 = update_ftp_user_quota(user)
        logger.info('Exit code: {}'.format(exit_code_2))


@receiver(post_save, sender=User)
def _update_user_proftpd_config(sender, instance, created, **kwargs):
    if kwargs['raw']:
        # https://github.com/django/django/commit/18a2fb19074ce6789639b62710c279a711dabf97
        return

    user = instance

    if not created and not user.is_superuser and user.ftp_enabled:
        if user.ftp_password_has_changed:
            logger.info('user profile updated ftp password, updating proftpd user password')
            exit_code = update_ftp_user_password(user)
            logger.info('Exit code: {}'.format(exit_code))

        if user.ftp_quota_has_changed:
            logger.info('user updated ftp password, updating proftpd user quota')
            exit_code = update_ftp_user_quota(user)
            logger.info('Exit code: {}'.format(exit_code))
