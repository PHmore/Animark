from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from .serializers import AnimeResponseSerializer
from .anime_service import AnimeService
from rest_framework.views import APIView
from rest_framework.response import Response

class AnimeListViefdsfw(ListView):
    template_name = 'animes/anime_list.html'

    # Aqui é passado o nome do objeto que será acessado pelo Html
    context_object_name = 'anime_list'
    paginate_by = 10  # Número de animes por página
    print("Mostrar top animes")

    def get_queryset(self):
        page_number = self.request.GET.get('page', 1)
        print(page_number)
        anime_list = AnimeService.get_anime_list(page_number)
        # print(anime_list)

        # Para retornar somente a data a qual é nomeada pelo contexto e enviada para o html
        return anime_list
        # page_number = self.request.GET.get('page',1)
        # data = AnimeService.get_anime_list(page_number)
        # return data['data'] if 'data' in data else []

class AnimeListView(APIView):
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
            
            # Agora você pode usar data_list, pagination_data e status_code conforme necessário
            print("Lista de dados:", data_list)
            print("Dados de paginação:", pagination_data)
            print("Código de status:", status_code)

            return render(request,'animes/anime_list.html',{'anime_data':serialized_data.get('data', []),'page_obj':serialized_data.get('pagination', {}),})
        else:
            serialized_data = serializer.errors
            errors = serializer.errors
            print("Erros de validação:", errors)
            # Retorne uma resposta de erro adequada, se necessário
            return Response(errors, status=400)

class AnimeInfo(APIView):
    print("Será exibida informações sobre o anime aqui")
class AnimeSrcView(ListView):
    template_name = 'animes/anime_search.html'
    context_object_name = 'animes'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return AnimeService.search_anime(query)
        return []
    
# Classes sem uso de api 
# animes/views.py

# class AnimeListView(ListView):
#     model = Anime
#     template_name = 'animes/anime_list.html'
#     context_object_name = 'animes'
#     print("Puxou a view 2")

# class AnimeCreateView(CreateView):
#     model = Anime
#     form_class = AnimeForm
#     template_name = 'animes/anime_form.html'
#     success_url = reverse_lazy('anime_list')

# class AnimeUpdateView(UpdateView):
#     model = Anime
#     form_class = AnimeForm
#     template_name = 'animes/anime_form.html'
#     success_url = reverse_lazy('anime_list')
