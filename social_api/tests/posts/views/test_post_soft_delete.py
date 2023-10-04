from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from social_api.posts.models import Post
from social_api.users.models import CustomUser


class PostSoftDeleteAPIViewTest(TestCase):
    CURRENT_DATE = timezone.now()

    VALID_USER_DATA = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword',
    }

    VALID_POST_DATA = {
        'content': 'This is for test',
        'timestamps': CURRENT_DATE,
        'status': 'Deleted',
    }

    def setUp(self):
        self.user = CustomUser.objects.create_user(**self.VALID_USER_DATA)
        user_data = {
            'author_id': self.user.id,
        }
        self.post = Post.objects.create(**self.VALID_POST_DATA, **user_data)

        # Creating a client to send requests
        self.client = APIClient()

        # Authentication of the user
        self.client.force_authenticate(user=self.user)

    def test_soft_delete__when_post_exists__expect_to_be_soft_deleted(self):
        url = reverse('soft delete post', kwargs={'pk': self.post.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Whether "soft_deleted" post is in db
        self.post.refresh_from_db()
        self.assertTrue(self.post.status, 'Deleted')
        self.assertIsNotNone(self.post.deleted_at)

    def test_soft_delete__when_post_does_not_exist__expect_to_raise(self):
        # Ако се опитате да изтриете несъществуващ пост, трябва да получите 404 Not Found
        url = reverse('soft delete post', kwargs={'pk': 9999})

        self.client.force_authenticate(user=self.user)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
