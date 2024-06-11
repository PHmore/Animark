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
            print("Id do anime na consulta a API: ",anime_id)
            print(anime_data)
            return anime_data
        return anime_data

    @classmethod
    def get_search_anime(cls, query):
        response = requests.get(f'{cls.BASE_URL}/anime/', params={'q': query})
        if response.status_code == 200:
            return response.json()['data']
        return []
