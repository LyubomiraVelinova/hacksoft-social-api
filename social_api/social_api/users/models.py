from django.db import models
from django.contrib.auth import models as auth_models


class CustomUser(auth_models.AbstractUser):
    MAX_LEN_NAME = 200

    email = models.EmailField(unique=True)
    name = models.CharField(
        max_length=MAX_LEN_NAME,
        blank=True,
        null=True,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
    )
    is_sandboxed = models.BooleanField(default=True)

