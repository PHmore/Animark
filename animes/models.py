from django.db import models

class Anime(models.Model):
    title = models.CharField(max_length=255)
    watched = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Episodio(models.Model):
    anime = models.ForeignKey(Anime, related_name='episodios', on_delete=models.CASCADE)
    episode_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255, blank=True, null=True)
    watched = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('anime', 'episode_number')

    def __str__(self):
        return f"{self.anime.title} - Episódio {self.episode_number}"
