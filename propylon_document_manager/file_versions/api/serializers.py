from rest_framework import serializers
from file_versions.models import FileVersion
from propylon_document_manager.utils.global_value import GlobalValue


class FileVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileVersion
        fields = [GlobalValue.FileName, GlobalValue.FileVersion, GlobalValue.FileSize, GlobalValue.FileType,
                  GlobalValue.FileUrl, GlobalValue.FileNameHash, GlobalValue.FileDesc, GlobalValue.FileUuid]
        # fields = "__all__"


class FileVersionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileVersion
        fields = [GlobalValue.FileName, GlobalValue.FileVersion, GlobalValue.FileSize, GlobalValue.FileType,
                  GlobalValue.FileUrl, GlobalValue.FileNameHash, GlobalValue.FileDesc, GlobalValue.FileUuid,
                  GlobalValue.FIleCreateTime]
        # fields = "__all__"
