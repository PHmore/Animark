from django.contrib import admin
from django.urls import path,include
from todo_list.views import *

# animes/urls.py
from django.urls import path

urlpatterns = [
    path('', AnimeTaskList.as_view(), name='to_do_list'),
    path('excluir/<int:pk>/',deleteTask.as_view(), name='excluir-task'),
    path('marcar/<int:anime_id>/<int:episode_id>/',updateTask.as_view(), name='marcar-ep'),
    path('api/', APIListarTask.as_view(), name='api-listar_animes'),
    path('api/excluir/<int:pk>/', APIDeletarTask.as_view(), name='api-deletar_animes'),
    path('api/marcar/<int:anime_id>/<int:episode_id>/', APIAtualizarTask.as_view(), name='api-atualizar_episodios'),
    # path('api/', APIListarVeiculos.as_view(), name='api-listar-veiculos'),

    # Api para deletra para ser usada pelo app 
    # path('api/<int:pk>/', APIDeletarVeiculos.as_view(),name='api-deletar')
]
