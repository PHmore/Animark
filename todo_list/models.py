# todo_list/models.py

from django.db import models
from animes.models import Anime, Episodio

class Task(models.Model):
    title = models.CharField(max_length=255)
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    
    # Relacionamentos com Anime, Temporada e Episodio
    anime = models.ForeignKey(Anime, related_name='tasks', on_delete=models.CASCADE, blank=True, null=True)
    episodio = models.ForeignKey(Episodio, related_name='tasks', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

