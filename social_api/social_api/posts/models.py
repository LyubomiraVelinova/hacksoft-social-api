from django.db import models

from social_api.users.models import CustomUser


class Post(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    content = models.TextField(
        null=False,
        blank=False,
    )
    timestamps = models.DateTimeField()
    is_deleted = models.BooleanField(
        default=False
    )
    is_published = models.BooleanField(
        default=False,
    )
    is_draft = models.BooleanField(
        default=True,
    )


class Like(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
