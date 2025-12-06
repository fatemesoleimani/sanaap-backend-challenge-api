from django.db import models


class UserRoleChoices(models.TextChoices):
    admin = 'admin'
    editor = 'editor'
    viewer = 'viewer'
