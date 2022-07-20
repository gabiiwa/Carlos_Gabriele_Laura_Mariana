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

# valida dados do login, me permitindo ver qual é o usuário atual
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Login
        fields = "__all__"
# A tabela de visulização me permitirá pontuar por visulização
class VisualizacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Visualizacao
        fields = "__all__"

class RankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Estudante
        fields = ['nome', 'pontuacao']

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Professor
        fields = ['nome']

class EstudanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Estudante
        fields = ['nome']

class TituloSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Titulo
        fields = ['nome', 'qtdPontos']        