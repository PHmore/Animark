# animes/serializers.py
from rest_framework import serializers
from animes.models import Anime, Episodio

class EpisodioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episodio
        fields = '__all__'

class AnimeSerializer(serializers.ModelSerializer):
    episodios = EpisodioSerializer(many=True, read_only=True)

    class Meta:
        model = Anime
        fields = '__all__'
