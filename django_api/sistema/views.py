# from asyncio.windows_events import NULL
from django.shortcuts import render

from rest_framework import viewsets
from sistema import serializers
from sistema import models
from rest_framework.response import Response
import requests
import datetime



class PostagemViewSet(viewsets.ModelViewSet):
    queryset = models.Postagem.objects.all().order_by('dataHora')
    serializer_class = serializers.PostagemSerializer
    #post
    def create(self, request):
        serializer = serializers.PostagemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            #salva os dados no banco
             serializer.save()
             #####Estudante########
             #pega os dados que foram enviados pela requisição post
             data = request.data
             #pega o id correspondente aestudante que fez o post para poder acessar a pontuação
             estudante_id = data.get("fkusuario")
             estudante_obj = models.Estudante.objects.get(id=estudante_id)
             #atualizando a pontuação
             estudante_obj.pontuacao += 15
             estudante_obj.save()
             #loop pra procurar tarefas do tipo postagem
            #  lista
             return Response(serializer.data)
class PostagemArmazenadaViewSet(viewsets.ModelViewSet):
    queryset = models.PostagemArmazenada.objects.all().order_by('post_date')
    serializer_class = serializers.PostagemArmazenadaSerializer
    def create(self, request):
        serializer = serializers.PostagemArmazenadaSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = request.data
            postArm = models.PostagemArmazenada.objects.get(id=data.get("id"))
            print('\n data de postagem:{}\n'.format(data.get("post_date")))
            # if data.get("post_date") == "":
            #    postArm.post_date = datetime.datetime.now()
            #    postArm.programada = 1
            #    postArm.save()
            # else:
            #     postArm.programada = 0
            #     postArm.save() 
            return Response(serializer.data)
    def list(self, request):
        #só postar se não for programada
        #caso contrario, precisa comparar o dia e hora 
        queryset = models.PostagemArmazenada.objects.all().order_by('post_date')
        serializer = serializers.PostagemArmazenadaSerializer(queryset, many=True)
        data_send = serializer.data
        print("\nEsta sendo mandado:{}\n".format(data_send))
        return Response(serializer.data)
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