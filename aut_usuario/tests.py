# tests/test_views.py

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class AuthTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', first_name='Test', email='test@example.com')
        self.token = Token.objects.create(user=self.user)

    def test_login(self):
        url = reverse('api-login')  # Certifique-se de que a URL do login seja correta
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.data['email'], self.user.email)

    def test_register(self):
        url = reverse('api-cadastro')  # Certifique-se de que a URL do registro seja correta
        data = {
            'email': 'new@example.com',
            'password': 'newpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['email'], 'new@example.com')

        # Verifique se o usuário foi realmente criado
        user = User.objects.get(email='new@example.com')
        self.assertIsNotNone(user)

    def test_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('api-logout')  # Certifique-se de que a URL do logout seja correta
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['mensagem'], 'Logout realizado com sucesso')
