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
        fields = ['titulo','texto','dataHora','fkusuario']
    
#tabela de serialização de tarefa
class TarefaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tarefa
        fields = ['tipo', 'fkestudante']

#tabela de serialização de comentário
class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comentario
        fields = ['texto','fkestudante', 'content_type', 'object_id']          