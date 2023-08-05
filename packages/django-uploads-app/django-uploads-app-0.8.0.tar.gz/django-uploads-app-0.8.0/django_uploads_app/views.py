import logging
import os

from django.http import Http404
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.utils.encoding import iri_to_uri
from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import generics, viewsets, permissions, parsers, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend

from django_sso_app.core.apps.users.utils import fetch_remote_user, create_local_user_from_remote_backend

from .permissions import is_staff

from .settings import USERS_FOLDER, NGINX_X_ACCEL_REDIRECT
from .utils import get_nginx_file_response, get_file_mimetype

from .exceptions import FileNotLoaded
from .forms import FileUploadForm
from .functions import arg_to_bool
from .models import Link, Upload, FileUpload, UploadType
from .serializers import LinkSerializer, UploadSerializer, UploadTypeSerializer
from .filters import UploadFilter

logger = logging.getLogger('apps.uploads')

User = get_user_model()

CURRENT_DIR = os.getcwd()
GROUP_DETAIL_URL_NAME = 'django_sso_app_group:rest-detail'


class APIRoot(APIView):
    """
    API Root.
    """

    # permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        try:
            return Response({
                'stats': reverse('stats', request=request, format=format),
                'upload-types': reverse('django_uploads:upload-type-list', request=request,
                                        format=format),
                'uploads': reverse('django_uploads:upload-list', request=request,
                                   format=format),
                'groups': reverse(GROUP_DETAIL_URL_NAME, request=request, format=format)
            })

        except:
            logger.exception('Error getting api-root')


class UploadTypeViewSet(viewsets.ModelViewSet):
    """
    Return upload types.
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = UploadTypeSerializer

    lookup_field = 'slug'

    def get_queryset(self):
        return UploadType.get_user_upload_types(self.request.user).order_by('id')


class UploadViewSet(viewsets.ModelViewSet):
    """
    Upload viewset.
    """
    serializer_class = UploadSerializer
    lookup_field = 'uuid'
    filter_backends = (DjangoFilterBackend,)
    filter_class = UploadFilter

    def get_queryset(self):
        if is_staff(self.request.user):
            return Upload.objects.all()

        return Upload.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        logger.info('Creating upload')

        # staff user can create upload for others
        user_sso_id = self.request.GET.get('user_sso_id', None)

        if user_sso_id is not None and is_staff(self.request.user):
            requesting_user = User.objects.filter(sso_app_profile__sso_id=user_sso_id).first()

            # user never seen, fetching from remote backend
            if requesting_user is None:
                logger.info('User "{}" not in DB, fetching remote'.format(user_sso_id))

                requesting_user_object = fetch_remote_user(user_sso_id)
                requesting_user = create_local_user_from_remote_backend(requesting_user_object)

            logger.info('User "{}" ask to create upload for "{}"'.format(self.request.user, requesting_user))

        else:
            requesting_user = self.request.user

        instance = serializer.save(user=requesting_user)

        file_received = False

        if instance.file_url is not None:
            logger.info(
                'Creating upload from file url {}'.format(instance.file_url))
            file_received = True

        elif instance.file_base64 is not None:
            logger.info('Creating upload from file base64')
            file_received = True

        elif instance.file_path is not None:
            logger.info(
                'Creating upload from file path {}'.format(instance.file_path))

            file_path = os.path.join(str(settings.PRIVATE_ROOT),
                                     instance.file_path)

            if Upload.objects.filter(file_path=instance.file_path).exclude(pk=instance.pk).count() > 0:
                logger.warning('User "{}" is trying to link non owned file in path "{}"'.format(
                    requesting_user,
                    file_path
                ))

                instance.delete()

                raise NotFound()

            if os.path.exists(file_path):
                user_sso_id_by_path = instance.file_path.lstrip('users' + os.path.sep).split(os.path.sep, 1)[0]

                if user_sso_id_by_path != instance.user.sso_id:
                    logger.warning('User "{}" is trying to link non owned file in path "{}"'.format(
                        requesting_user,
                        file_path
                    ))

                    instance.delete()

                    raise NotFound()

                file_upload = instance.create_file_upload(request=self.request,
                                                          uploaded_at=instance.created_at)
                file_upload.file_data.name = file_path
                file_upload.save()

                file_received = True

            else:
                error_msg = 'File path {} not found'.format(file_path)
                logger.warning(error_msg)

                instance.delete()

                raise NotFound(error_msg)

        else:
            file_upload = instance.create_file_upload(self.request)

            logger.info('FileUpload instance: {}'.format(file_upload))

        if file_received:
            if arg_to_bool(self.request.GET.get('get_download_link', False)):
                active_forever = arg_to_bool(
                    self.request.GET.get('active_forever', False))
                times_downloadable = int(
                    self.request.GET.get('times_downloadable', 1))
                is_public = arg_to_bool(self.request.GET.get('public', False))
                comment = self.request.GET.get('comment', None)

                instance.create_download_link(active_forever=active_forever,
                                              times_downloadable=times_downloadable,
                                              is_public=is_public,
                                              comment=comment)

            instance.refresh_from_db()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,
                                         context={
                                             'request': self.request
                                         })
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            logger.exception('Error creating Upload')

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)


class SetUploadParsedAt(APIView):
    """
    Set upload parsed_at property
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, uuid, *args, **kwargs):
        """
        Set Upload as parsed
        """
        try:
            upload = Upload.objects.get(uuid=uuid)

        except Upload.DoesNotExist:
            raise Http404()

        else:
            logger.info('User "{}" asked to set upload "{}" as parsed'.format(request.user, upload))
            upload.parsed_at = timezone.now()
            upload.save()

        return Response(status=status.HTTP_200_OK)


class SetUploadSuccessfullyParsed(APIView):
    """
    Set upload parsed_at property and successfully_parsed=True
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, uuid, *args, **kwargs):
        """
        Set Upload as parsed
        """
        try:
            upload = Upload.objects.get(uuid=uuid)

        except Upload.DoesNotExist:
            raise Http404()

        else:
            logger.info('User "{}" asked to set upload "{}" as successfully parsed'.format(request.user, upload))
            upload.parsed_at = timezone.now()
            upload.successfully_parsed = True
            upload.save()

        return Response(status=status.HTTP_200_OK)


class SetUploadUnsuccessfullyParsed(APIView):
    """
    Set upload parsed_at property and successfully_parsed=False
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, uuid, *args, **kwargs):
        """
        Set Upload as parsed
        """
        try:
            upload = Upload.objects.get(uuid=uuid)

        except Upload.DoesNotExist:
            raise Http404()

        else:
            logger.info('User "{}" asked to set upload "{}" as unsuccessfully parsed'.format(request.user, upload))
            upload.parsed_at = timezone.now()
            upload.successfully_parsed = False
            upload.save()

        return Response(status=status.HTTP_200_OK)


class LinkViewSet(viewsets.ModelViewSet):
    """
    Link viewset.
    """
    serializer_class = LinkSerializer

    lookup_field = 'uuid'

    def get_queryset(self):
        if is_staff(self.request.user):
            return Link.objects.all()

        return Link.objects.filter(upload__user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        return super(LinkViewSet, self).retrieve(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(LinkViewSet, self).destroy(self, request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super(LinkViewSet, self).partial_update(self, request, *args, **kwargs)


class CreateDownloadLink(generics.GenericAPIView):
    """
    Return new download link.
    """
    queryset = Upload.objects.all()
    serializer_class = LinkSerializer

    def post(self, request, uuid, *args, **kwargs):
        """
        Generates a download link usable 'times_downloadable' times
        """
        try:
            upload = get_object_or_404(Upload, uuid=uuid)

            logger.info('Creating download link for {}'.format(upload))

            serializer = self.get_serializer(data=request.data,
                                             context={
                                                 'request': self.request
                                             })

            if serializer.is_valid(raise_exception=True):
                active_until = serializer.data.get('active_until', request.data.get('active_until', None))
                times_downloadable = serializer.data.get('times_downloadable', request.data.get('times_downloadable', None))
                is_public = serializer.data.get('is_public', request.data.get('is_public', True))
                shares = serializer.data.get('shares', request.data.get('shares', []))

                comment = serializer.data.get('comment', request.data.get('comment', None))

                if active_until == '':
                    active_until = None
                if times_downloadable == '':
                    times_downloadable = None
                if comment == '':
                    comment = None

                active_forever = serializer.data.get('active_forever',
                                                     request.data.get('active_forever',
                                                                      (active_until is None
                                                                       and times_downloadable is None)))

                new_link = upload.create_download_link(
                    active_forever=active_forever,
                    active_until=active_until,
                    times_downloadable=times_downloadable,
                    is_public=is_public,
                    shares=shares,
                    comment=comment)

                serializer = LinkSerializer(instance=new_link,
                                            context={
                                                'request': self.request
                                            })

        except Exception as e:
            logger.exception('Error creating download link: {}'.format(e))
            raise Http404('Not found')

        else:
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class FileUploadView(APIView):
    """
    File upload.
    """
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, uuid, *args, **kwargs):
        try:
            file_upload = FileUpload.objects.get(uuid=uuid)

            if file_upload.uploaded_at is None:
                form = FileUploadForm(request=request, file_upload=file_upload)

                return render(self.request, 'django_uploads_app/file_upload.html',
                              {'request': request, 'form': form})
            else:
                raise Http404('Not found')

        except:
            logger.exception('Error getting file-upload')
            raise Http404('Not found')

    def post(self, request, uuid, *args, **kwargs):
        try:
            file_upload = FileUpload.objects.get(uuid=uuid)

            form = FileUploadForm(request.POST, request.FILES, request=request, file_upload=file_upload)

            if form.is_valid():
                created_file_upload = form.save(file_upload=file_upload)

                """
                if request.content_type == 'application/json':
                    return HttpResponseRedirect(reverse('django_uploads:upload-detail',
                                                        kwargs={'uuid': created_file_upload.upload.uuid}))
                else:
                    return HttpResponseRedirect(reverse('django_uploads:file-upload-success'))
                """
                return HttpResponseRedirect(reverse('django_uploads:upload-detail',
                                                    kwargs={'uuid': created_file_upload.upload.uuid}))

            else:
                form_errors = dict(form.errors.items())

                if '__all__' in form_errors.keys():
                    if len(form_errors['__all__']) == 1:
                        parsed_errors = form_errors['__all__'][0]
                    else:
                        parsed_errors = form_errors['__all__']
                else:
                    parsed_errors = form_errors

                return Response(parsed_errors, status=400)

        except:
            logger.exception('Error creating file-upload')

            return Response('Malformed file', status=400)


class GetProtectedFileView(APIView):
    """
    Return file.
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request, secret, *args, **kwargs):
        """
        Download file given secret
        """
        now = timezone.now()
        link = Link.objects.filter(secret=secret).first()

        logger.info('Get protected file from link: {}'.format(link))

        if link is not None and link.active:

            if not link.is_available_for_user(request.user):
                logger.warning('User {} tried to download link not available'.format(request.user))

                raise Http404('Not found')

            try:
                upload = link.upload

                if upload.file_url not in (None, ''):
                    logger.info('Serving by redirect')

                    response = HttpResponseRedirect(upload.file_url)

                elif link.upload.file_base64 not in (None, ''):
                    logger.info('Serving base64')

                    response = HttpResponse(link.upload.file_base64)

                elif upload.file_path not in (None, ''):
                    logger.info('Serving file_path')

                    if NGINX_X_ACCEL_REDIRECT:
                        logger.info('Serving by nginx')
                        file_name = upload.file_path.rsplit(os.path.sep, 1).pop()
                        file_path = upload.file_path.rstrip(file_name)

                        nginx_path = '/private/{}{}'.format(file_path,
                                                            iri_to_uri(file_name))
                        logger.info('nginx path "{}"'.format(nginx_path))

                        response = get_nginx_file_response(nginx_path)
                    else:
                        logger.info('Serving by django')

                        file_path = '{}{}{}'.format(settings.PRIVATE_ROOT,
                                                    os.path.sep,
                                                    upload.file_path)

                        logger.info('file path "{}"'.format(file_path))

                        file_data = open(file_path, 'rb')
                        content_type = getattr(upload, 'file_mime', None)

                        if content_type is None:
                            content_type = get_file_mimetype(file_path)

                        response = HttpResponse(file_data, content_type=content_type[0])

                    response['Content-Disposition'] = 'attachment; filename={}'.format(upload.file_name)

                elif upload.file_upload is not None:
                    logger.info('Serving file_upload')

                    file_upload = upload.file_upload

                    if file_upload.file_url is not None:
                        logger.info('Serving by redirect')

                        response = HttpResponseRedirect(file_upload.file_url)

                    elif file_upload.file_data is not None:
                        logger.info('Serving by file_data')

                        file_data = file_upload.file_data

                        if NGINX_X_ACCEL_REDIRECT:
                            logger.info('Serving by nginx')

                            nginx_path = '/private/{}'.format(iri_to_uri(file_data.name))
                            logger.info('nginx path "{}"'.format(nginx_path))

                            response = get_nginx_file_response(nginx_path)
                        else:
                            logger.info('Serving by django')

                            file_data_path = os.path.join(USERS_FOLDER, file_data.name)

                            content_type = getattr(upload, 'file_mime', None)
                            if content_type is None:
                                content_type = get_file_mimetype(file_data_path)

                            response = HttpResponse(file_data, content_type=content_type[0])

                        response['Content-Disposition'] = 'attachment; filename="{}"'.format(link.upload.file_name)

                    else:
                        raise FileNotLoaded()

                else:
                    raise FileNotLoaded()

            except Exception as e:
                logger.exception('Error getting protected file')

                raise Http404('Not found')

            else:
                link.times_downloaded += 1
                link.updated_at = now
                link.downloaded_at = now

                link.save()

            return response

        raise Http404('Not found')
