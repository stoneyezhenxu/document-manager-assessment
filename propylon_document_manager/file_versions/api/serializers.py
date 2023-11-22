from rest_framework import serializers

from propylon_document_manager.file_versions.models import FileVersion

class FileVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileVersion
        fields = "__all__"
