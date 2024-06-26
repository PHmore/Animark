from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import UpdateView, DeleteView, TemplateView
from rest_framework.generics import ListAPIView ,DestroyAPIView, UpdateAPIView
from django.urls import reverse_lazy
from animes.models import Anime, Episodio
from .forms import MarcarForm

from .serializers import AnimeSerializer, EpisodioSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


# Tornar o login obrigatório
from django.contrib.auth.mixins import LoginRequiredMixin

# Importações para este arquivo
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse, Http404

# Importações para tokens
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import permissions, viewsets, status
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated

# Ver como modificar para que o retorno seja por ordem de atualização e os completos fiquem no final

# Talvez seja possível fazer para que todas as operações GET, POST, PUT E DELETE fiquem em uma só classe e sejam métodos da API

class AnimeTaskList(LoginRequiredMixin, TemplateView):
    template_name = 'todo_list/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        animes = Anime.objects.filter(user=user)
        anime_dict = {anime: anime.episodios.all().order_by('-assistido', 'numero') for anime in animes}
        context['anime_dict'] = anime_dict
        return context

class updateTask(LoginRequiredMixin, UpdateView):
    model = Episodio
    template_name = 'todo_list/home.html'
    form_class = MarcarForm

    def get_object(self, queryset=None):
        anime_id = self.kwargs.get('anime_id')
        episode_id = self.kwargs.get('episode_id')
        anime = get_object_or_404(Anime, pk=anime_id, user=self.request.user)
        return get_object_or_404(Episodio, pk=episode_id, anime=anime)

    def form_valid(self, form):
        form.save()
        return redirect(reverse_lazy('to_do_list'))

class deleteTask(LoginRequiredMixin, DeleteView):
    model = Anime
    success_url = reverse_lazy('to_do_list')

    def get_queryset(self):
        return Anime.objects.filter(user=self.request.user)

# Talvez adicionar um método para quando o anime for interamente assistido

class APIListarTask(ListAPIView):
    """
    View para listar instâncias de animes (por meio da API REST)
    """

    serializer_class = AnimeSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
        
    def get_queryset(self):
        user = self.request.user
        return Anime.objects.filter(user=user).order_by('-updated_at')

class APIDeletarTask(DestroyAPIView):
    serializer_class = AnimeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Anime.objects.filter(user=user)


class APIAtualizarTask(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def put(self, request, anime_id, episode_id):
        try:
            anime = Anime.objects.get(id=anime_id, user=request.user)
            episodio = Episodio.objects.get(anime=anime, id=episode_id)
        except (Anime.DoesNotExist, Episodio.DoesNotExist):
            return Response({"error": "Anime or Episodio not found"}, status=status.HTTP_404_NOT_FOUND)

        episodio.assistido = not episodio.assistido
        episodio.save()

        return Response({"message": "Episodio updated successfully"}, status=status.HTTP_200_OK)



# class APICriarTask(viewsets.ViewSet):
#     """
#     View para criar novas tasks (por meio da API REST)
#     """
#     authentication_classes = [TokenAuthentication, SessionAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     @action(detail=False, methods=['post'])
#     def create_task(self, request):
#         print("A criação de tasks será movida para essa view")
#         return Response({"message": "Task creation logic here"})
