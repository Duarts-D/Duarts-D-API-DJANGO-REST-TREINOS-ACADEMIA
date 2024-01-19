from rest_framework import serializers
from apps.academia.models import TreinoModel
from collections import defaultdict
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class TreinoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreinoModel
        fields = ['id','treino_nome','usuario']

    usuario = serializers.StringRelatedField(read_only=True)

    def create(self,validated_data):
        validated_data['usuario'] = self.context['request'].user
        validate = super().create(validated_data)
        return validate