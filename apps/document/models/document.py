from django.db import models

from core.base_model import BaseModel


class Document(BaseModel):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="docs/")
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
