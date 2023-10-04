from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from social_api.users.models import CustomUser


class RegisterUserAPITest(TestCase):
    VALID_USER_DATA = {
        'email': 'test@example.com',
        'password': 'testpassword',
        'username': 'testuser',
    }

    DUPLICATE_VALID_USER_DATA = {
        'email': 'test@example.com',
        'password': 'testpassword1',
    }

    INVALID_USER_DATA = {
        'email': 'invalid_email',
        'password': 'testpassword',
        'username': 'testuser',
    }

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')

    def create_user(self, user_data):
        response = self.client.post(self.register_url, data=user_data, format='json')
        return response

    def test_register_user__when_valid_data__expect_to_be_registered(self):
        response = self.create_user(self.VALID_USER_DATA)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

    def test_register_user__when_invalid_data__expect_bad_request(self):
        response = self.create_user(self.INVALID_USER_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_register_user__when_duplicate_email__expect_bad_request(self):
        self.create_user(self.VALID_USER_DATA)
        response = self.create_user(self.DUPLICATE_VALID_USER_DATA)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_register_user_is_sandboxed__when_successful_registration__expect_true(self):
        response = self.create_user(self.VALID_USER_DATA)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

        user = CustomUser.objects.get(email=self.VALID_USER_DATA['email'])
        self.assertTrue(user.is_sandboxed)
