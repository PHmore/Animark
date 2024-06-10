import requests

class AnimeService:
    BASE_URL = 'https://api.jikan.moe/v4'

    @classmethod
    def get_anime_list(cls, page_number):
        response = requests.get(f'{cls.BASE_URL}/top/anime?page={page_number}')
        
        if response.status_code == 200:
            response_data = response.json()
            # anime_data = response_data.get('data', [])
            # print(anime_data)
            # pagination_data = response_data.get('pagination', {})
            # print(pagination_data)
            # status = response_data.get('status', None)
            # print(status)
            
            # return {
            #     'data':response_data,
            #     'pagination':pagination_data,
            #     'status':status
            # }
            return response_data
        
        return None

    @classmethod
    def get_anime_info(cls, anime_id):
        response = requests.get(f'{cls.BASE_URL}/anime/{anime_id}')
        if response.status_code == 200:
            anime_data = response.json()
            return {'title': anime_data.get('title', 'Unknown'), 'image_url': anime_data.get('image_url', '')}
        return {'title': 'Unknown', 'image_url': ''}

    @classmethod
    def search_anime(cls, query):
        response = requests.get(f'{cls.BASE_URL}/anime', params={'q': query})
        if response.status_code == 200:
            return response.json()['data']
        return []
