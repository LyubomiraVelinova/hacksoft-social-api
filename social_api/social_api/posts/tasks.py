# Write your Celery tasks here

from celery import current_task
from datetime import datetime, timedelta

from social_api.posts.models import Post


# @task
# def gard_delete_soft_deleted_posts():
#     ten_days_ago = datetime.now() - timedelta(days=10)
#     soft_deleted_posts = Post.objects.filter(is_deleted=True, deleted_at__lt = ten_days_ago)
#     soft_deleted_posts.delete()

# Watch the CELERY lection