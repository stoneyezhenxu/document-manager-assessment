import logging
import os
from django.http import FileResponse
from django.contrib.auth import get_user_model
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from propylon_document_manager.utils import utils
from propylon_document_manager.utils.global_value import GlobalValue
from file_versions.models import FileVersion
from .serializers import FileVersionSerializer, FileVersionListSerializer

User = get_user_model()


# @login_required
class FileVersionViewSet(RetrieveModelMixin, ListModelMixin, CreateModelMixin, GenericViewSet):
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
        instances = self.get_queryset().order_by('-create_at')
        serializer = FileVersionListSerializer(instance=instances, many=True)
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
        # get resource by file_url_hash_code with revision  -> GET /api/files/{file_url_hash_code}/?revision=2
        revision = request.query_params.dict().get('revision', '')
        file_name_hash = kwargs.get(self.lookup_field)
        logging.info(
            "FileVersionViewSet retrieve is called! ->revision={}, file_name_hash:{}".format(revision, file_name_hash))
        if revision and revision != 'null':
            revision = int(revision)
            instances = self.get_queryset().filter(file_name_hash=file_name_hash, file_version=revision)
        else:
            instances = self.get_queryset().filter(file_name_hash=file_name_hash)
        if not instances.exists():
            return Response(status=status.HTTP_204_NO_CONTENT, data={'No data!'})
        instances = instances.order_by(f'-{GlobalValue.FileVersion}')
        serializer = FileVersionListSerializer(instance=instances, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(methods=['GET'], detail=False)
    def content(self, request):
        file_uuid = request.query_params.dict().get('file_uuid', '').replace('-', '')
        file_type = request.query_params.dict().get('file_type', '')
        file_name = request.query_params.dict().get('file_name', '')
        logging.info(
            'content -> request.data:{}, file_uuid:{}, file_type:{}, file_name:{} '.format(request.data, file_uuid,
                                                                                           file_type, file_name))
        local_file_path = utils.get_local_file_path(file_uuid=file_uuid, file_type=file_type, file_name=file_name)
        if not os.path.exists(local_file_path):
            logging.info('file not exist local_file_path:{}'.format(local_file_path))
            return Response(status=status.HTTP_204_NO_CONTENT, data='file not exist!')
        response = FileResponse(open(local_file_path, 'rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{file_uuid}"'
        return response
