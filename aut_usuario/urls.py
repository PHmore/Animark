from django.contrib import admin
from django.urls import path,include
from aut_usuario.views import *



urlpatterns = [
    path('',Login.as_view(),name='index'),
    path('logout/',Logout.as_view(),name='logout'),
    path('cadastro/',Cadastro.as_view(),name='cadastro'),
    path('api/login/', LoginAPI.as_view(), name='api-login'),
    path('api/logout/', LogoutAPI.as_view(), name='api-logout'),
    path('api/cadastro/', CadastroAPI.as_view(), name='api-cadastro'),
]
