from datetime import datetime, timedelta

from celery import shared_task

from social_api.posts.models import Post

''''
An automatic process that “hard” deletes all posts 
that were “soft” deleted 10+ days ago.
'''


@shared_task
def hard_delete_soft_deleted_posts():
    ten_days_ago = datetime.now() - timedelta(days=10)
    soft_deleted_posts = Post.objects.filter(status='Deleted', deleted_at__lt=ten_days_ago)

    for post in soft_deleted_posts:
        post.delete()
