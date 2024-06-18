from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from .serializers import AnimeResponseSerializer, AnimeInfoResponseSerializer
from .anime_service import AnimeService
from rest_framework.views import APIView
from rest_framework.response import Response
from animes.models import Anime, Episodio

# Falta serializar este adicionar botões de adicionar e mostrar na página html corretamente


from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Anime

from rest_framework import status

class AnimeListView(LoginRequiredMixin,APIView):
    def get(self, request, *args, **kwargs):
        page_number = request.GET.get('page', 1)
        anime_data = AnimeService.get_anime_list(page_number)
        
        # Serializar os dados da resposta da API
        serializer = AnimeResponseSerializer(data=anime_data)
        
        if serializer.is_valid():
            serialized_data = serializer.data
            # Acesso aos dados serializados
            data_list = serialized_data.get('data', [])
            pagination_data = serialized_data.get('pagination', {})
            status_code = serialized_data.get('status')
            
            # Obter todos os IDs de animes no banco de dados
            db_anime_ids = set(Anime.objects.values_list('mal_id', flat=True))
            
            # Iterar sobre os dados da API e adicionar o campo 'in_list'
            for anime in data_list:
                anime_id = anime.get('mal_id')
                anime['in_list'] = anime_id in db_anime_ids
            
            # Renderizar a página com os dados serializados
            return render(request, 'animes/anime_list.html', {
                'anime_data': data_list,
                'page_obj': pagination_data,
            })
        else:
            serialized_data = serializer.errors
            errors = serializer.errors
            print("Erros de validação:", errors)
            # Retorne uma resposta de erro adequada, se necessário
            return Response(errors, status=400)
# db_anime_ids = set(Anime.objects.values_list('mal_id', flat=True)): Usamos um conjunto (set) para armazenar os IDs de animes do banco de dados para uma verificação rápida de pertencimento (in operation). Conjuntos em Python são otimizados para verificação de pertencimento.
# Iteração e Adição de in_list: Para cada anime recebido da API (data_list), verificamos se o mal_id está presente em db_anime_ids. Se estiver, definimos anime['in_list'] como True; caso contrário, como False.
# Renderização da Página: No retorno da renderização da página, passamos data_list atualizado, que agora inclui o campo in_list, junto com outros dados necessários como pagination_data.

class AnimeInfo(LoginRequiredMixin, APIView):
    
    def get(self, request):
    
        query = request.GET.get('data_id')
        print("Anime id: ",query)
        anime_info = AnimeService.get_anime_info(query)

        # Como neste caso é passado uma lista e não um dicionário por conter apenas um item o many deve ser definido como False sendo o inverso dado como True
        serializer = AnimeInfoResponseSerializer(data=anime_info)
        
        print("\n\nA info foi serializada: ",serializer)

        if serializer.is_valid():
            serialized_data = serializer.data
            data_list = serialized_data.get('data', [])
            print("\n\nA info foi serializada: ",data_list)
            return JsonResponse(serialized_data)
        print("\n\nA info foi  não serializada!!!! ")
        return []

class AnimeSrcView(LoginRequiredMixin,APIView):
    
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('anime_nome')
        print("Query:", query)
        
        anime_src = AnimeService.get_search_anime(query)
        
        # Verificando a estrutura dos dados retornados
        # print("Dados recebidos:", anime_src)
        print("Quantidade de dados recebidos:", len(anime_src))
        
        serializer = AnimeResponseSerializer(data=anime_src)
        
        if serializer.is_valid():
            serialized_data = serializer.data
            # print("\n\nA info foi serializada: ", serialized_data)
            return render(request, 'animes/anime_list.html', {
                'anime_data': serialized_data.get('data', []),
                'page_obj': serialized_data.get('pagination', {}),
            })
        
        print("\n\nA info não foi serializada!!!! ", serializer.errors)
        return Response(serializer.errors)
      
class AnimeTaskCreate(LoginRequiredMixin,View):
    def post(self,request):
        titulo_anime = request.POST.get('title')
        # descricao_anime = request.POST.get('descricao_anime')
        # episodios = request.POST.getlist('episodios')
        episodios = request.POST.get('episodes')
        print("Titulo: ",titulo_anime," Episidios: ",episodios)
        episodios = int(episodios)
        mal_id = request.POST.get('mal_id')
        mal_id = int(mal_id)
        novo_anime = Anime.objects.create(mal_id=mal_id,titulo=titulo_anime,assistido=False,)

        for ep in range(1, episodios+1):
            numero_episodio = ep

            Episodio.objects.create(
                anime=novo_anime,
                numero=numero_episodio,
            )
        
        # return render()
        return redirect("/to_do_list")

class AnimeListAPI(APIView):
    def get(self, request, *args, **kwargs):
        page_number = request.GET.get('page', 1)
        anime_data = AnimeService.get_anime_list(page_number)
        serializer = AnimeResponseSerializer(data=anime_data)
        if serializer.is_valid():
            serialized_data = serializer.data
            data_list = serialized_data.get('data', [])
            pagination_data = serialized_data.get('pagination', {})
            db_anime_ids = set(Anime.objects.values_list('mal_id', flat=True))
            for anime in data_list:
                anime_id = anime.get('mal_id')
                anime['in_list'] = anime_id in db_anime_ids
            return Response({
                'anime_data': data_list,
                'page_obj': pagination_data,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnimeInfoAPI(APIView):
    def get(self, request):
        query = request.GET.get('data_id')
        anime_info = AnimeService.get_anime_info(query)
        serializer = AnimeInfoResponseSerializer(data=anime_info)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnimeSrcAPI(APIView):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('anime_nome')
        anime_src = AnimeService.get_search_anime(query)
        serializer = AnimeResponseSerializer(data=anime_src)
        if serializer.is_valid():
            serialized_data = serializer.data
            return Response({
                'anime_data': serialized_data.get('data', []),
                'page_obj': serialized_data.get('pagination', {}),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnimeTaskCreateAPI(APIView):
    def post(self, request):
        titulo_anime = request.data.get('title')
        episodios = request.data.get('episodes')
        episodios = int(episodios)
        mal_id = request.data.get('mal_id')
        mal_id = int(mal_id)
        novo_anime = Anime.objects.create(mal_id=mal_id, titulo=titulo_anime, assistido=False)
        for ep in range(1, episodios + 1):
            Episodio.objects.create(anime=novo_anime, numero=ep)
        return Response({'mensagem': 'Anime criado com sucesso'}, status=status.HTTP_201_CREATED)