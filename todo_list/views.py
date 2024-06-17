from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from animes.models import Anime, Episodio
from .forms import MarcarForm


# Ver como modificar para que o retorno seja por ordem de atualização e os completos fiquem no final

class AnimeTaskList(TemplateView):
    template_name='todo_list/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animes = Anime.objects.all()
        # Aqui definiremos para que o retorno seja feito em ordem de update
        anime_dict = {anime: anime.episodios.all().order_by('numero') for anime in animes}
        # anime_dict = {animes: animes}
        context['anime_dict'] = anime_dict
        print("Retornando as seguintes tasks: ",context)
        return context

class createTask ():
    def post():
        print("A criação de tasks será movida para essa view")

class updateTask (UpdateView):
    model = Episodio
    template_name = 'todo_list/home.html'
    # success_url = reverse_lazy('to_do_list')

    form_class = MarcarForm
    # fields = []  # Nenhum campo será exibido no formulário
    template_name = 'to_do_list/toggle_assistido.html'  # Você pode criar um template vazio ou omiti-lo

    def get_object(self, queryset=None):
        anime_id = self.kwargs.get('anime_id')
        episode_id = self.kwargs.get('episode_id')
        anime = get_object_or_404(Anime, pk=anime_id)
        return get_object_or_404(Episodio, pk=episode_id, anime=anime)

    def form_valid(self, form):
        form.save()
        return redirect(reverse_lazy('to_do_list'))

    # def get_queryset(request, anime_id, episode_id):
    #     anime = get_object_or_404(Anime, pk=anime_id)
    #     episode = get_object_or_404(Episodio, pk=episode_id, anime=anime)
        
    #     # Inverte o valor do booleano de assistido
    #     episode.assistido = not episode.assistido
    #     episode.save()
        
    #     # Redireciona de volta para a lista de tarefas
    #     return reverse_lazy('to_do_list')
    
class deleteTask (DeleteView):
    model = Anime
    # template_name = 'todo_list/home.html'
    success_url = reverse_lazy('to_do_list')

# Talvez adicionar um método para quando o anime for interamente assistido