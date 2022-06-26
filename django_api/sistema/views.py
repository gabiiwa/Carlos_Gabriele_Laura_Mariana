from django.shortcuts import render

from rest_framework import viewsets
from sistema import serializers
from sistema import models
from rest_framework.response import Response
import requests

class PostagemViewSet(viewsets.ModelViewSet):
    queryset = models.Postagem.objects.all().order_by('dataHora')
    serializer_class = serializers.PostagemSerializer
    #post
    def create(self, request):
        serializer = serializers.PostagemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            #salva os dados no banco
             serializer.save()
             #pega os dados que foram enviados pela requisição post
             data = request.data
             #pega o id correspondente aestudante que fez o post para poder acessar a pontuação
             estudante_id = data.get("fkusuario")
             estudante_obj = models.Estudante.objects.get(id=estudante_id)
             #atualizando a pontuação
             estudante_obj.pontuacao += 15
             estudante_obj.save()
             #setar data de postagem
             #loop pra procurar tarefas do tipo postagem
            #  lista
             return Response(serializer.data)
class PostagemArmazenadaViewSet(viewsets.ModelViewSet):
    queryset = models.PostagemArmazenada.objects.all().order_by('post_date')
    serializer_class = serializers.PostagemArmazenadaSerializer
    # def create(self, request):
    #     serializer = serializers.PostagemArmazenadaSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #          serializer.save()
             
    #          return Response(serializer.data)
    # def list(self, request):
    #     #só postar se não for programada
    #     #caso contrario, precisa comparar o dia e hora 
class TarefaViewSet(viewsets.ModelViewSet):
    queryset = models.PostagemArmazenada.objects.all().order_by('post_date')
    serializer_class = serializers.PostagemArmazenadaSerializer



#############Páginas que dependem de dados do banco###################
def home(request):
    response = requests.get('http://127.0.0.1:8000/postagem/')
    data = response.json()
    estudantes = [models.Estudante.objects.get(id=dict_est['fkusuario']).nome for dict_est in data ]
    #inserindo qual foi a estudante que realizoua postagem
    for post,i in zip(data,range(len(estudantes))):
        post['nome']=estudantes[i]
    return render(request, 'home.html', {'data': data})