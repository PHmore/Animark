from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from .serializers import AnimeResponseSerializer, AnimeInfoResponseSerializer
from .anime_service import AnimeService
from rest_framework.views import APIView
from rest_framework.response import Response
from animes.models import Anime, Episodio
from django.views.generic import View

class AnimeSrcView(ListView):
    template_name = 'animes/anime_search.html'
    context_object_name = 'animes_src'
    print("Pesquisar nome do anime")
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        print(query)
        anime_src = AnimeService.get_search_anime(query)
        print(anime_src)
        if query:
            return anime_src
        return []

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
      
class AnimeTaskCreate(View):
    def post(self,request):
        titulo_anime = request.POST.get('title')
        # descricao_anime = request.POST.get('descricao_anime')
        # episodios = request.POST.getlist('episodios')
        episodios = request.POST.get('episodes')
        print("Titulo: ",titulo_anime," Episidios: ",episodios)
        episodios = int(episodios)
        novo_anime = Anime.objects.create(titulo=titulo_anime,assistido=False,)

        for ep in range(1, episodios+1):
            numero_episodio = ep

            Episodio.objects.create(
                anime=novo_anime,
                numero=numero_episodio,
            )
        
        return HttpResponse('Anime e episodios criados com sucesso')




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
