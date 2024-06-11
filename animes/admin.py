# animes/admin.py

from django.contrib import admin
from .models import Anime, Episodio

class EpisodioInline(admin.TabularInline):
    model = Episodio
    extra = 1

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    inlines = [EpisodioInline]

@admin.register(Episodio)
class EpisodioAdmin(admin.ModelAdmin):
    list_display = ('numero',  'assistido')
    list_filter = ('assistido', 'numero')
    search_fields = ('numero',)
