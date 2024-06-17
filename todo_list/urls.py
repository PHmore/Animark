from django.contrib import admin
from django.urls import path,include
from todo_list.views import *

# animes/urls.py
from django.urls import path

urlpatterns = [
    path('', AnimeTaskList.as_view(), name='to_do_list'),
    path('excluir/<int:pk>/',deleteTask.as_view(), name='excluir-task'),
     path('marcar/<int:anime_id>/<int:episode_id>/',updateTask.as_view(), name='marcar-ep'),
]
