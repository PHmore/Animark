from django.db import models
from datetime import datetime

class Anime(models.Model):
    titulo = models.CharField(max_length=255)
    assistido = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0} - {1}'.format (
            self.titulo,
            self.assistido,
        )

    def tempo_assistindo(self):
        return datetime.now().day - self.created_at

    @property
    def anime_novo(self):
        return self.created_at == datetime.now().day
    
class Episodio(models.Model):
    anime = models.ForeignKey(Anime, related_name='episodios', on_delete=models.CASCADE)
    numero = models.PositiveIntegerField()
    assistido = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('anime', 'numero')

    def __str__(self):
        return f"{self.anime.titulo} - Episódio {self.numero}"
