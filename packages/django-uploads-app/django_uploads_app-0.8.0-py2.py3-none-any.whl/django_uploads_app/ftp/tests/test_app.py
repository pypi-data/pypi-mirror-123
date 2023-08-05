import os
from pathlib import Path

from django.urls import reverse
from django.contrib.auth import get_user_model

from filer.models import File as FilerFile

# from rest_framework import status

from ...tests import APITestFactory
from ...models import Upload, Link

from ..utils import parse_user_files

User = get_user_model()


class TestFtp(APITestFactory):
    def setUp(self):
        super(TestFtp, self).setUp()

        self.user_folder_ftp_path = os.path.join(self.user_folder_path, 'ftp')

    def test_user_folder_creation_on_access(self):
        """
        Creates user related folder on first access
        """

        self.perform_user_login()

        response = self.client.get('/', format='json')

        self.assertTrue(os.path.exists(self.user_folder_ftp_path), 'user ftp folder not created')

    def test_fpt_uploaded_file_creates_upload_model(self):
        self.perform_user_login()

        Path(os.path.join(self.user_folder_ftp_path, 'ftp_file.txt')).touch()

        _parsed_files = parse_user_files(self.user)

        relative_path = os.path.join('users', self.user.sso_id) + os.sep + os.path.join('ftp', 'ftp_file.txt')

        self.assertTrue(Upload.objects.filter(file_path=relative_path).count() == 1, 'cannot link to ftp uploaded file')

    def test_fpt_uploaded_file_creates_upload_model_once(self):
        self.perform_user_login()

        Path(os.path.join(self.user_folder_ftp_path, 'ftp_file.txt')).touch()

        _parsed_files = parse_user_files(self.user)

        relative_path = os.path.join('users', self.user.sso_id) + os.sep + os.path.join('ftp', 'ftp_file.txt')

        self.assertTrue(Upload.objects.filter(file_path=relative_path).count() == 1, 'cannot link to ftp uploaded file')

        Path(os.path.join(self.user_folder_ftp_path, 'ftp_file.txt')).touch()

        _parsed_files = parse_user_files(self.user)

        self.assertTrue(Upload.objects.filter(file_path=relative_path).count() == 1, 'cannot link to ftp uploaded file')
        self.assertTrue(Upload.objects.count() == 1, 'more than one Upload created')

    def test_fpt_uploaded_file_creates_filer_file(self):
        self.perform_user_login()

        Path(os.path.join(self.user_folder_ftp_path, 'ftp_file.txt')).touch()

        _parsed_files = parse_user_files(self.user)

        relative_path = os.path.join('users', self.user.sso_id) + os.sep + os.path.join('ftp', 'ftp_file.txt')

        self.assertTrue(FilerFile.objects.filter(file=relative_path).count() == 1, 'cannot find filer file for ftp uploaded file')
