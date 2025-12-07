from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

from core.base_model import BaseModel

minio_storage = S3Boto3Storage()


class Document(BaseModel):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="", storage=minio_storage)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
