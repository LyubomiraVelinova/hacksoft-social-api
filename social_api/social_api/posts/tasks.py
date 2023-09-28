# Write your Celery tasks here
from datetime import datetime, timedelta

from celery import shared_task

from social_api.posts.models import Post


# Изтриване на "soft deleted" постове автоматично:
#
# За автоматичното изтриване на "soft deleted" постове, можете да използвате Django management команда и plan за задачи (scheduler) като Celery. Във вашия план за задачи, постъпвайте по следния начин:
#
# Извличайте всички "soft deleted" постове, чиито дата на "soft delete" е преди 10+ дни.
# Изтривайте тези постове от базата данни (т.е., направете "hard delete").

@shared_task
def hard_delete_soft_deleted_posts():
    ten_days_ago = datetime.now() - timedelta(days=10)
    soft_deleted_posts = Post.objects.filter(is_deleted=True, deleted_at__lt=ten_days_ago)
    soft_deleted_posts.delete()

