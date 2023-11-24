from django.db import models
from django.conf import settings

from propylon_document_manager.utils.global_value import GlobalValue
from propylon_document_manager.utils.utils import get_uuid




class FileVersion(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file_name = models.fields.CharField(max_length=512, verbose_name='file_name')
    file_version = models.fields.IntegerField(verbose_name='file_version',default=0)
    file_size = models.fields.CharField(max_length=20, verbose_name='file_size')
    file_type = models.fields.CharField(choices=GlobalValue.FileTypes_choices, max_length=15, verbose_name='file_type',default='others')
    file_url = models.fields.CharField(max_length=512, verbose_name='file_url')
    create_at = models.DateTimeField(auto_now_add=True,verbose_name='create_time')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='update_time')
    deleted_at = models.DateTimeField(auto_now=True,verbose_name='delete_time')
    file_uuid = models.UUIDField(unique=True, default=get_uuid, verbose_name='file_uuid')
    file_name_hash = models.fields.CharField(max_length=32, verbose_name='file_uuid')
    file_desc = models.fields.CharField(max_length=512,default='', verbose_name='file_desc')

    def __str__(self):
        return self.file_name
