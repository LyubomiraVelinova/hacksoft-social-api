from django.contrib.auth import get_user_model
from django.db import models

from social_api.users.models import CustomUser


class Post(models.Model):
    STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Published', 'Published'),
    )

    MAX_LEN_CHOICES = 15

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
        default=False,
    )
    # My implementation-as a user created a post can choose whether to publish or draft
    status = models.CharField(
        max_length=MAX_LEN_CHOICES,
        choices=STATUS_CHOICES,
        default='Draft',
        null=True,
        blank=True,
    )
    likes = models.ManyToManyField(
        CustomUser,
        related_name='liked_posts',
        blank=True,
        null=True,
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
