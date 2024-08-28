from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse

class TestLoginAPI(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345', email='test@example.com')

    def test_login(self):
        url = reverse('api-login')
        data = {'username': 'testuser', 'password': '12345'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], 'testuser')

    def test_login_invalid_credentials(self):
        url = reverse('api-login')
        data = {'username': 'testuser', 'password': 'wrongpassword'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)

    def test_login_missing_fields(self):
        url = reverse('api-login')
        data = {'username': 'testuser'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)

class TestLogoutAPI(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_logout(self):
        url = reverse('api-logout')

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(key=self.token.key).exists())

class TestCadastroAPI(APITestCase):

    def test_cadastro(self):
        url = reverse('api-cadastro')
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], 'newuser')

    def test_cadastro_usuario_existente(self):
        User.objects.create_user(username='existinguser', password='existingpassword', email='existing@example.com')
        url = reverse('api-cadastro')
        data = {
            'username': 'existinguser',
            'password': 'existingpassword',
            'email': 'existing@example.com',
            'first_name': 'Existing',
            'last_name': 'User'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)