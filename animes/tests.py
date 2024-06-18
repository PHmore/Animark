from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from animes.models import Anime, Episodio

# Create your tests here.

# Fazer teste da API tanto da view que a consome quando do anime_service.py
# Fazer teste da model tbm

class AnimeTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.anime = Anime.objects.create(mal_id=1, titulo='Test Anime', assistido=False)
        for ep in range(1, 6):
            Episodio.objects.create(anime=self.anime, numero=ep)

    def test_anime_list(self):
        url = reverse('api-anime-list')
        response = self.client.get(url, {'page': 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('anime_data', response.data)
        self.assertIn('page_obj', response.data)

    def test_anime_info(self):
        url = reverse('api-anime-info')
        response = self.client.get(url, {'data_id': self.anime.mal_id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)

    def test_anime_src(self):
        url = reverse('api-anime-src')
        response = self.client.get(url, {'anime_nome': 'Test Anime'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('anime_data', response.data)

    def test_anime_task_create(self):
        url = reverse('api-anime-task-create')
        data = {
            'title': 'New Anime',
            'episodes': 12,
            'mal_id': 123
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('mensagem', response.data)
        self.assertEqual(response.data['mensagem'], 'Anime criado com sucesso')