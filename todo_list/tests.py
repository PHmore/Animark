from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from animes.models import Anime, Episodio
from .serializers import AnimeSerializer

class TestAPIListarTask(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.anime1 = Anime.objects.create(user=self.user, titulo='Anime 1')
        self.anime2 = Anime.objects.create(user=self.user, titulo='Anime 2')

    def test_listar_animes(self):
        url = reverse('api-listar_animes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['titulo'], 'Anime 2')
        self.assertEqual(response.data[1]['titulo'], 'Anime 1')

    def test_listar_animes_unauthorized(self):
        self.client.credentials()  # Remove as credenciais para simular um usuário não autenticado
        url = reverse('api-listar_animes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TestAPIDeletarTask(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.anime = Anime.objects.create(user=self.user, titulo='Anime 1')

    def test_deletar_anime(self):
        url = reverse('api-deletar_animes', kwargs={'pk': self.anime.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Anime.objects.filter(pk=self.anime.pk).exists())

    def test_deletar_anime_unauthorized(self):
        self.client.credentials()  # Remove as credenciais para simular um usuário não autenticado
        url = reverse('api-deletar_animes', kwargs={'pk': self.anime.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TestAPIAtualizarTask(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.anime = Anime.objects.create(user=self.user, titulo='Anime 1')
        self.episodio = Episodio.objects.create(anime=self.anime, numero=1, assistido=False)

    def test_atualizar_episodio(self):
        url = reverse('api-atualizar_episodios', kwargs={'anime_id': self.anime.pk, 'episode_id': self.episodio.pk})
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.episodio.refresh_from_db()
        self.assertTrue(self.episodio.assistido)

    def test_atualizar_episodio_invalid_ids(self):
        url = reverse('api-atualizar_episodios', kwargs={'anime_id': 999, 'episode_id': 999})
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_atualizar_episodio_unauthorized(self):
        self.client.credentials()  # Remove as credenciais para simular um usuário não autenticado
        url = reverse('api-atualizar_episodios', kwargs={'anime_id': self.anime.pk, 'episode_id': self.episodio.pk})
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)