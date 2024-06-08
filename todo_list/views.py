from django.shortcuts import render
from django.views.generic import ListView

class TodoListView(ListView):
    print("Listar animes")

# Create your views here.

# Aqui será feito as funções da todo list