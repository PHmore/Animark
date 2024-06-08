from django.contrib import admin
from django.urls import path,include
from todo_list.views import *



urlpatterns = [
    path('',Login.as_view(),name='index'),
    path('logout/',Logout.as_view(),name='logout'),
    path('cadastro/',Cadastro.as_view(),name='cadastro'),
    path('cadastro/',Cadastro.as_view(),name='cadastro'),
]