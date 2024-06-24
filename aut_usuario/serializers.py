# serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'senha']
        extra_kwargs = {'senha': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            # username=validated_data['email'],  # Usando email como username
            # email=validated_data['email'],
            senha=validated_data['senha']
        )
        return user
