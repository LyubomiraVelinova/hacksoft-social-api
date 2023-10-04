from django.test import TestCase

from social_api.posts.models import Post, Like
from social_api.users.models import CustomUser
from social_api.users.serializers import ProfileUserRetrieveSerializer


class ProfileUserRetrieveSerializerTest(TestCase):
    VALID_USER_DATA = {
        'email': 'test@example.com',
        'username': 'test',
        'first_name': 'Lyubomira',
        'last_name': 'Velinova',
        'description': 'Take me in your team, you won`t be sorry.',
        'profile_picture': None,
    }

    def setUp(self):
        self.user = CustomUser.objects.create_user(**self.VALID_USER_DATA)
        self.post_1 = Post.objects.create(author=self.user, content='Post 1 content')
        self.post_2 = Post.objects.create(author=self.user, content='Post 2 content')
        self.like_1 = Like.objects.create(user=self.user, post=self.post_1)
        self.like_2 = Like.objects.create(user=self.user, post=self.post_2)

    def test_total_likes_and_posts__when_valid_data__expect_to_be_2(self):
        serializer = ProfileUserRetrieveSerializer(instance=self.user)

        self.assertEqual(serializer.get_total_likes(self.user), self.user.liked_posts.count())
        self.assertEqual(serializer.get_total_posts(self.user), self.user.posts.count())
