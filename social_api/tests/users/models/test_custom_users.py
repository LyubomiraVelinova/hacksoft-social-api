from django.db.utils import DataError
from django.test import TestCase


from social_api.users.models import CustomUser


class CustomUserTest(TestCase):
    VALID_USERS_DATA = {
        'email': 'test@example.com',
        'password': 'testpassword',
        'first_name': 'Test',
        'last_name': 'Case',
        'description': 'This is a TestCase',
        'username': 'testuser',
    }

    INVALID_FIRST_NAME_USERS_DATA = {
        'email': 'test@example.com',
        'password': 'testpassword',
        'first_name': 'T' * 31,
        'last_name': 'Case',
        'description': 'This is a TestCase',
        'username': 'testuser',
    }

    def test_create_user__when_valid_data__expect_to_be_created(self):
        user = CustomUser.objects.create_user(**self.VALID_USERS_DATA)
        self.assertIsInstance(user, CustomUser)
        self.assertEqual(user.email, self.VALID_USERS_DATA['email'])
        self.assertEqual(user.first_name, self.VALID_USERS_DATA['first_name'])
        self.assertEqual(user.last_name, self.VALID_USERS_DATA['last_name'])
        self.assertEqual(user.description, self.VALID_USERS_DATA['description'])

    def test_first_name_max_length__when_more_than_30_char__expect_to_raise(self):
        with self.assertRaises(DataError):
            CustomUser.objects.create_user(**self.INVALID_FIRST_NAME_USERS_DATA)

