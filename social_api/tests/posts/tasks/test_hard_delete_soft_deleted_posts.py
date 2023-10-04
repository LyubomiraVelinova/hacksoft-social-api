from datetime import datetime, timedelta
from django.test import TestCase
from django.utils import timezone

from social_api.posts.models import Post
from social_api.posts.tasks import hard_delete_soft_deleted_posts
from social_api.users.models import CustomUser


class HardDeleteSoftDeletedPostsTests(TestCase):
    CURRENT_DATE = timezone.now()
    OLD_DATE = CURRENT_DATE - timedelta(days=11)

    VALID_USER_DATA = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword',
    }

    VALID_HARD_DELETE_POST_DATA = {
        'content': 'This is for hard delete test',
        'status': 'Deleted',
        'deleted_at': OLD_DATE,
    }

    VALID_SOFT_DELETE_POST_DATA = {
        'content': 'This is for soft delete test',
        'status': 'Deleted',
        'deleted_at': CURRENT_DATE,
    }

    VALID_NOT_DELETED_POST_DATA = {
        'content': 'This post is not deleted',
        'status': 'Published',
        'deleted_at': None,
    }

    def setUp(self):
        self.user = CustomUser.objects.create_user(**self.VALID_USER_DATA)

    def create_post(self, post_data):
        user_data = {
            'author_id': self.user.id,
        }
        post = Post.objects.create(**post_data, **user_data)
        return post

    def test_hard_delete__when_post_is_deleted_11_days_ago__expected_to_be_deleted(self):
        post = self.create_post(self.VALID_HARD_DELETE_POST_DATA)

        # Calling Celery for deleting "soft deleted" posts and waiting for it to finish
        result = hard_delete_soft_deleted_posts.apply()
        result.get()  # Wait for the Celery task to complete

        post_exists = Post.objects.filter(pk=post.pk).exists()
        self.assertFalse(post_exists, 'Post should be deleted')

    def test_soft_delete__when_post_is_deleted_now__expect_not_to_be_deleted(self):
        post = self.create_post(self.VALID_SOFT_DELETE_POST_DATA)

        result = hard_delete_soft_deleted_posts.apply()
        result.get()

        post_exists = Post.objects.filter(pk=post.pk).exists()
        self.assertTrue(post_exists, 'Post should be deleted')

    def test_hard_delete__when_posts_are_soft_deleted__expect_only_soft_deleted_to_be_deleted(self):

        for i in range(3):
            soft_post = self.create_post(self.VALID_HARD_DELETE_POST_DATA)

        for i in range(3):
            non_soft_post = self.create_post(self.VALID_NOT_DELETED_POST_DATA)

        result = hard_delete_soft_deleted_posts.apply()
        result.get()

        soft_deleted_post_count = Post.objects.filter(is_deleted=True).count()
        non_soft_deleted_post_count = Post.objects.filter(is_deleted=False).count()
        self.assertEqual(soft_deleted_post_count, 0, 'Soft deleted posts should be deleted')
        self.assertEqual(non_soft_deleted_post_count, 3, 'Non-soft deleted posts should not be deleted')
