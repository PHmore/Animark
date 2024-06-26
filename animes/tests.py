import unittest
from animes.anime_service import AnimeService  # Substitua 'myapp' pelo nome correto do seu aplicativo


from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from animes.models import Anime, Episodio  # Substitua 'myapp' pelo nome correto do seu aplicativo

class TestAnimeListAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_get_anime_list(self):
        url = reverse('api-anime-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('anime_data', response.data)

    def test_get_anime_list_unauthorized(self):
        self.client.credentials()
        url = reverse('api-anime-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TestAnimeTaskCreateAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_create_anime(self):
        url = reverse('api-anime-task-create')
        data = {'title': 'New Anime', 'episodes': 12, 'mal_id': 12345}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_anime = Anime.objects.filter(user=self.user, titulo='New Anime').first()
        self.assertIsNotNone(created_anime)
        self.assertEqual(created_anime.episodios.count(), 12)

    def test_create_anime_unauthorized(self):
        self.client.credentials()
        url = reverse('api-anime-task-create')
        data = {'title': 'New Anime', 'episodes': 12, 'mal_id': 12345}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestAnimeServiceRealAPI(unittest.TestCase):

    def test_get_anime_list_success(self):
        result = AnimeService.get_anime_list(1)
        self.assertIsNotNone(result)
        self.assertIn('data', result)
        self.assertIsInstance(result['data'], list)

    def test_get_search_anime_success(self):
        result = AnimeService.get_search_anime('naruto', 1)
        self.assertIsNotNone(result)
        self.assertIn('data', result)
        self.assertIsInstance(result['data'], list)

    def test_get_search_anime_failure(self):
        # Teste para um termo de pesquisa que provavelmente não retornará resultados
        result = AnimeService.get_search_anime('asdfghjkl', 1)
        self.assertIsNotNone(result)
        self.assertIn('data', result)
        self.assertIsInstance(result['data'], list)
        self.assertEqual(len(result['data']), 0)

if __name__ == '__main__':
    unittest.main()
