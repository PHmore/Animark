from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse_lazy

from rest_framework import generics
from .models import Anime
from .serializers import AnimeSerializer

from django.views.generic import CreateView, UpdateView, ListView
from .models import Task
from .forms import TaskForm

class TaskListView(ListView):
    model = Task
    template_name = 'todo_list/task_list.html'
    context_object_name = 'tasks'

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'todo_list/task_form.html'
    success_url = reverse_lazy('task_list')

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'todo_list/task_form.html'
    success_url = reverse_lazy('task_list')
