from django.db.models import fields
from rest_framework import serializers
from sistema import models

"""
Serializers define a forma de representação dos dados.
Faz a transformação dos dados de json pra Python e o processo contrário.
"""

# tabela de serializacao de postagem

class PostagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Postagem
        fields = "__all__"  