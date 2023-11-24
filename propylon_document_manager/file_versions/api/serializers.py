from rest_framework import serializers

from file_versions.models import FileVersion
from propylon_document_manager.utils.global_value import GlobalValue


class FileVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileVersion
        fields = [GlobalValue.FileName, GlobalValue.FileVersion, GlobalValue.FileSize, GlobalValue.FileType,
                  GlobalValue.FileUrl, GlobalValue.FileNameHash]
