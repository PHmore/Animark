from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Anime(models.Model):
    
# Caso seja colocado um novo campo posteriormente em alguma model é necessário definir um valor padrão pra mesma ou se pode ser null ou blank

# null=True: Permite que o campo no banco de dados aceite valores nulos. Isso significa que, se nenhum valor for fornecido para mal_id, o banco de dados permitirá que esse campo seja nulo.
# blank=True: Permite que o formulário de criação ou edição não exija um valor para esse campo. Ou seja, no formulário Django, você pode deixar o campo mal_id em branco sem gerar um erro de validação.
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1,)
    mal_id = models.PositiveIntegerField(null=True, blank=True)
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
