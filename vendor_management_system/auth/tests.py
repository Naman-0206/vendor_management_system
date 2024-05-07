from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class RegisterUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        data = {
            'username': 'test_user',
            'password': 'test_password'
        }

        response = self.client.post('/api/register/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn('token', response.data)

        user_exists = User.objects.filter(username='test_user').exists()
        self.assertTrue(user_exists)

        token_obj = Token.objects.filter(user__username='test_user').first()
        token_exists = token_obj is not None
        self.assertTrue(token_exists)
        self.assertEqual(response.data['token'], token_obj.pk)

    def test_duplicate_user_registration(self):
        User.objects.create_user(
            username='existing_user', password='test_password')

        data = {
            'username': 'existing_user',
            'password': 'test_password'
        }

        response = self.client.post('/api/register/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('username', response.data)

        token_exists = Token.objects.filter(
            user__username='existing_user').exists()
        self.assertFalse(token_exists)
