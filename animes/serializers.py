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
    episodes = serializers.IntegerField(allow_null=True, default=1)
    status = serializers.CharField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get('episodes') is None:
            representation['episodes'] = 1
        return representation

# Aqui é feita a serialização do objeto como um todo
class AnimeResponseSerializer(serializers.Serializer):
    data = AnimeDataSerializer(many=True)
    pagination = serializers.DictField(required=False)
    status = serializers.IntegerField(required=False)

# Ao contrário do método acima este é para serializar itens únicos no caso uma lista
class AnimeInfoResponseSerializer(serializers.Serializer):
    data = AnimeDataSerializer(many=False)
    pagination = serializers.DictField(required=False)
    status = serializers.IntegerField(required=False)
