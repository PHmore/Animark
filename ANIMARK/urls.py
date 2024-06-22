from django.contrib import admin
from django.urls import path,include



urlpatterns = [
    # Incluindo as urls contidas em auth_usuario
    path('',include('aut_usuario.urls')),
	path('admin/',admin.site.urls),

    # Obs lembrar de adicionar a barra no final para que não seja um concatenação
    path('animes/',include('animes.urls')),
    path('to_do_list/',include('todo_list.urls')),
]