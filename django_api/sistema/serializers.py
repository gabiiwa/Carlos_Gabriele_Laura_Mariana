from django.db.models import fields
from rest_framework import serializers
from sistema import models

"""
Serializers define a forma de representação dos dados.
Faz a transformação dos dados de json pra Python e o processo contrário.
"""

# tabela de serializacao de postagem das alunas
class PostagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Postagem
        fields = ['titulo', 'texto', 'fkusuario']

#tabela de serialização de postagem das professoras
class PostagemArmazenadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PostagemArmazenada
        fields = ['titulo','texto','post_date','fkusuario',
                    'tag']