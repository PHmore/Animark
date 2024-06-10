from rest_framework import serializers

class ImageSerializer(serializers.Serializer):
    image_url = serializers.URLField()
    small_image_url = serializers.URLField()
    large_image_url = serializers.URLField()


# Aqui colocaremos quais dados usaremos para fazer a serialização de data
class AnimeDataSerializer(serializers.Serializer):
    mal_id = serializers.IntegerField()
    title = serializers.CharField()
    url = serializers.URLField()
    # synopsis = serializers.CharField()
    # Status
    # Ano
    # Outros dados interessantes adicionar aqui
    images = serializers.DictField(child=ImageSerializer())
    episodes = serializers.IntegerField()

# Aqui é feita a serialização do objeto como um todo
class AnimeResponseSerializer(serializers.Serializer):
    data = AnimeDataSerializer(many=True)
    pagination = serializers.DictField(required=False)
    status = serializers.IntegerField(required=False)
