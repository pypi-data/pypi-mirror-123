from pathlib import Path

import os
import json
import shutil

from django.contrib import auth

from django_sso_app.core.tests.factories import UserTestCase

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status

from filer.models.foldermodels import Folder

from .models import Upload, Link, UploadType
from .utils import get_user_folder_path

User = get_user_model()


class APITestFactory(UserTestCase):
    def setUp(self):
        self.base_upload_type, _created = UploadType.objects.get_or_create(name='File', slug='file', is_public=True)

        # user
        self.user_password = self._get_random_pass()
        self.user = self._get_new_user(password=self.user_password)
        self.user_folder_path = get_user_folder_path(self.user)

        self.valid_login = self._get_login_object(self.user.username, self.user_password)

        # staff
        self.staff_user_password = self._get_random_pass()
        self.staff_user = self._get_new_staff_user(password=self.staff_user_password)
        self.staff_user_folder_path = get_user_folder_path(self.staff_user)

        print('USER', self.user)
        print('STAFF USER', self.staff_user)

    def tearDown(self):
        shutil.rmtree(self.user_folder_path, ignore_errors=True)
        shutil.rmtree(self.staff_user_folder_path, ignore_errors=True)

    def perform_user_login(self):
        response = self.client.post(
            reverse('rest_login'),
            data=json.dumps(self.valid_login),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

        return response


class TestUploads(APITestFactory):
    def test_user_folder_creation_on_access(self):
        """
        Creates user related folder on first access
        """

        self.perform_user_login()

        _response = self.client.get('/', format='json')

        user_folder_uploads_path = os.path.join(self.user_folder_path, self.base_upload_type.slug)

        self.assertTrue(os.path.exists(user_folder_uploads_path), 'user upload folder not created')

    def test_create_upload_by_file_path(self):
        """
        Can create upload object
        """

        self.perform_user_login()

        folder_path = os.path.join(get_user_folder_path(self.user), 'folder')
        os.makedirs(folder_path, exist_ok=True)

        Path(os.path.join(self.user_folder_path, 'file', 'test.txt')).touch()

        file_path = 'users/{}/file/test.txt'.format(self.user.sso_id)
        file_name = 'test.txt'
        request_data = {
                'file_path': file_path,
                'file_name': file_name,
                'upload_type': 'file',
                'file_mime': 'text/plain'
                }

        response = self.client.post(reverse('django_uploads:upload-list') + \
                                    '?get_download_link=true&active_forever=true&public=true',
                                    request_data,
                                    format='json')

        new_upload = Upload.objects.filter(user=self.user).first()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Upload.objects.filter(user=self.user).count(), 1)
        self.assertEqual(new_upload.file_path, file_path)

    def test_max_times_downloadable(self):
        self.perform_user_login()

        folder_path = os.path.join(get_user_folder_path(self.user), 'folder')
        os.makedirs(folder_path, exist_ok=True)

        Path(os.path.join(self.user_folder_path, 'file', 'test.txt')).touch()

        file_path = 'users/{}/file/test.txt'.format(self.user.sso_id)
        file_name = 'test.txt'
        request_data = {
            'file_path': file_path,
            'file_name': file_name,
            'upload_type': 'file',
            'file_mime': 'text/plain'
        }

        response = self.client.post(reverse('django_uploads:upload-list'),
                                    request_data,
                                    format='json')
        print('RESP', response.json())

        new_upload = Upload.objects.filter(user=self.user).first()

        self.assertNotEqual(new_upload, None)

        link_request_data = {
            'times_downloadable': 5,
        }

        response2 = self.client.post(reverse('django_uploads:create-download-link',
                                             kwargs={'uuid': new_upload.uuid}),
                                     link_request_data,
                                     format='json')

        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        new_link = Link.objects.all().first()
        url3 = reverse('protected_file_download', kwargs={'secret': new_link.secret})

        i = 0
        while i < 5:
            response3 = self.client.get(url3)
            i += 1
            self.assertEqual(response3.status_code, status.HTTP_200_OK)

        response4 = self.client.get(url3)
        self.assertEqual(response4.status_code, status.HTTP_404_NOT_FOUND, 'can download even if already downloaded 5 times')

    def test_staff_user_can_create_upload_for_different_user(self):
        """
        Can create upload object for different user
        """

        folder_path = os.path.join(get_user_folder_path(self.user), 'file')
        os.makedirs(folder_path, exist_ok=True)

        Path(os.path.join(self.user_folder_path, 'file', 'test.txt')).touch()

        file_path = 'users/{}/file/test.txt'.format(self.user.sso_id)
        file_name = 'test.txt'
        request_data = {
                'file_path': file_path,
                'file_name': file_name,
                'upload_type': 'file',
                'file_mime': 'text/plain'
                }

        response = self.client.post(reverse('django_uploads:upload-list') +
                                    '?get_download_link=true&active_forever=true&public=true&user_sso_id={}'.format(self.user.sso_id),
                                    request_data,
                                    **self._get_new_api_token_headers(self.staff_user))

        new_upload = Upload.objects.filter(user=self.user).first()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Upload.objects.filter(user=self.user).count(), 1)
        self.assertEqual(new_upload.file_path, file_path)

    def test_user_filer_folders_creation_on_access(self):
        """
        Creates user related filer folders on first access
        """

        users_folder, _created = Folder.objects.get_or_create(name='users')

        self.perform_user_login()

        _response = self.client.get(
            '/', format='json')

        user_folder = Folder.objects.get(name=self.user.sso_id, parent=users_folder, owner=self.user)
        for ut in UploadType.objects.all():
            self.assertEqual(Folder.objects.filter(name=ut.slug, parent=user_folder).count(), 1,
                             'user filer folder "{}" not created'.format(ut.slug))
