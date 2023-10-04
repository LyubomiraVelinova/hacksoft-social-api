from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from social_api.posts.models import Post
from social_api.users.models import CustomUser


class PostTests(TestCase):
    CURRENT_DATE = timezone.now()

    VALID_USER_DATA = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword',
    }

    VALID_POST_DATA = {
        'content': 'This is for test',
        'timestamps': CURRENT_DATE,
    }

    INVALID_POST_DATA = {
        'content': '',
        'timestamps': CURRENT_DATE,
    }

    def setUp(self):
        self.user = CustomUser.objects.create_user(**self.VALID_USER_DATA)

    def test_create__when_valid__expect_to_be_created(self):
        user_data = {
            'author_id': self.user.id,
        }

        post = Post.objects.create(**self.VALID_POST_DATA, **user_data)
        self.assertIsNotNone(post.pk)

    def test_create__when_content_is_none__expect_to_raise(self):
        user_data = {
            'author_id': self.user.id,
        }

        with self.assertRaises(ValidationError):
            post = Post.objects.create(**self.INVALID_POST_DATA, **user_data)
            post.full_clean()
