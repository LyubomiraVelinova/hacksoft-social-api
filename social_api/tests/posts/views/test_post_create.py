from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from social_api.posts.models import Post
from social_api.users.models import CustomUser

User = get_user_model()


class PostCreateAPIViewTest(TestCase):
    CURRENT_DATE = timezone.now()

    VALID_USER_DATA = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword',
    }

    VALID_POST_DATA = {
        'content': 'This is for test',
        'status': 'Draft',
    }

    def setUp(self):
        self.user = CustomUser.objects.create_user(**self.VALID_USER_DATA)
        user_data = {
            'author_id': self.user.id,
        }

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_post__when_valid_data__expect_to_be_created(self):
        url = reverse('create post')
        response = self.client.post(url, data=self.VALID_POST_DATA, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.content, self.VALID_POST_DATA['content'])
        self.assertEqual(post.status, self.VALID_POST_DATA['status'])
        self.assertEqual(post.author, self.user)

    def test_create_post__when_invalid_data__expect_not_to_be_created(self):
        url = reverse('create post')
        incomplete_data = {'content': ''}
        response = self.client.post(url, data=incomplete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)

    def test_create_post__when_user_is_unauthenticated__expect_not_to_be_created(self):
        self.client.logout()
        url = reverse('create post')
        response = self.client.post(url, data=self.VALID_POST_DATA, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 0)
