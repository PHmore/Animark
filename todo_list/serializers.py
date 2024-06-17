# Exemplo de uso do serializers

# animes/serializers.py
from rest_framework import serializers
from .models import Anime

class AnimeSerializer(serializers.ModelSerializer):
    titulo = serializers.SerializerMethodField()
    assistido = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    class Meta:
        model = Anime
        fields = ['id', 'titulo']
