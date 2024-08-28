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
    # Exemplo de pesquisa
    def get_search_anime(cls,anime_nome,page=1):
        url = "https://api.jikan.moe/v4/anime"
        params = {
            'q': anime_nome,
            'page':page
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code}")
            return data


