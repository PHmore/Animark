from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse_lazy

from rest_framework import generics
from animes.models import Anime, Episodio

from django.views.generic import CreateView, UpdateView, ListView, TemplateView

class AnimeTaskList(TemplateView):
    template_name='todo_list/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animes = Anime.objects.all()
        anime_dict = {anime: anime.episodios.all() for anime in animes}
        context['anime_dict'] = anime_dict
        print("Retornando as seguintes tasks: ",context)
        return context