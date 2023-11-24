from django.shortcuts import render
import logging

from django.contrib.auth import get_user_model
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from propylon_document_manager.utils import utils
from propylon_document_manager.utils.global_value import GlobalValue
from file_versions.models import FileVersion
from .serializers import FileVersionSerializer

User = get_user_model()

class FileVersionViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FileVersionSerializer
    queryset = FileVersion.objects.all()
    lookup_field = "file_name_hash"

    def get_queryset(self, *args, **kwargs):
        # filter by user id
        return self.queryset.filter(user=self.request.user.id)

    def list(self, request, *args, **kwargs):
        # get resources  -> GET /api/users/files/
        logging.info("FileVersionViewSet -> list is called! ")
        instances = self.get_queryset()
        serializer = self.serializer_class(instance=instances, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request, *args, **kwargs):
        # post file  -> POST /api/users/files/
        logging.info("FileVersionViewSet -> create is called! ")
        request_data, error_infos = utils.valid_request_for_files_post(request_data=request.data)
        logging.info('request_data: {}'.format(request_data))

        serializer = self.serializer_class(data=request_data, context={"request": request.data})
        serializer.is_valid(raise_exception=True)
        user_existing_records = self.get_queryset().filter(file_name=request_data[GlobalValue.FileName]).order_by(
            f'-{GlobalValue.FileVersion}')
        file_version = user_existing_records[0].file_version + 1 if user_existing_records else 0
        serializer.save(user=self.request.user, file_version=file_version)

        response_data = []
        response_data.append(serializer.data)
        response_data.extend(self.serializer_class(instance=user_existing_records, many=True).data)

        # save cur file to local  -> /static/{file_type}/{file_name}/
        utils.save_file_to_local(file_uuid=request_data[GlobalValue.FileUuid],
                                 file_name=request_data[GlobalValue.FileName],
                                 file_type=request_data[GlobalValue.FileType],
                                 file_obj=request_data[GlobalValue.FileObj])

        return Response(status=status.HTTP_200_OK, data=response_data)

    def retrieve(self, request, *args, **kwargs):
        # get resource by file_name_hash  ->GET retrieve /api/user/files/file_uuid/
        file_name_hash = kwargs.get('file_name_hash')
        logging.info(
            "FileVersionViewSet retrieve is called! ->args:{}, kwargs: {} file_name_hash:{}".format(args, kwargs,
                                                                                                    file_name_hash))
        instances = self.get_queryset().filter(file_name_hash=file_name_hash)
        # Empty data
        if len(instances) == 0:
            return Response(status=status.HTTP_204_NO_CONTENT, data={'No data search by file_name_hash'})
        instances = instances.order_by(f'-{GlobalValue.FileVersion}')
        serializer = self.serializer_class(instance=instances, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(methods=["POST"], detail=False)
    def url(self, request):
        # get resource by url  -> POST /api/user/files/url/
        file_url = request.data.get('url')
        logging.info("FileVersionViewSet url is called! post -> /api/user/files/url/  file_url:{}".format(file_url))
        instances = self.get_queryset().filter(file_url=file_url)
        # Empty data
        if len(instances) == 0:
            return Response(status=status.HTTP_204_NO_CONTENT, data={'No data search by file_url'})

        instances = instances.order_by(f'-{GlobalValue.FileVersion}')
        serializer = self.serializer_class(instance=instances, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
