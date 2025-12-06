from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.user.choices import UserRoleChoices


class User(AbstractUser):
    role = models.CharField(max_length=10, choices=UserRoleChoices.choices, default=UserRoleChoices.viewer)
