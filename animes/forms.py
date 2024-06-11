# animes/forms.py

from django import forms
from .models import Anime, Temporada, Episodio

class AnimeForm(forms.ModelForm):
    class Meta:
        model = Anime
        exclude = []
