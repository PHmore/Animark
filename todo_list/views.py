from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse_lazy

from rest_framework import generics
from .models import Anime
from .serializers import AnimeSerializer

from django.views.generic import CreateView, UpdateView, ListView

class TaskListView(ListView):
    template_name='todo_list/home.html'
    context_object_name='animes_task'
    def get_queryset(self):
        print("Será mostrado as tasks pendentes")