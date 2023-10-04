from django.db import models

from social_api.users.models import CustomUser


class Post(models.Model):
    STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Published', 'Published'),
        ('Deleted', 'Deleted'),
    )

    MAX_LEN_CHOICES = 10

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    content = models.TextField(
        null=False,
        blank=False,
    )
    timestamps = models.DateTimeField(
        auto_now_add=True,
    )
    status = models.CharField(
        max_length=MAX_LEN_CHOICES,
        choices=STATUS_CHOICES,
        default='Draft',
    )
    likes = models.ManyToManyField(
        CustomUser,
        related_name='liked_posts',
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True
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
