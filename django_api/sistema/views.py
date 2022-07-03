# from asyncio.windows_events import NULL
from django.shortcuts import render

from rest_framework import viewsets,status
from sistema import serializers
from sistema import models
from rest_framework.response import Response
import requests
import datetime

import django

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

             data_atual = datetime.date.today()
             tarefa_check = models.Tarefa.objects.filter(fkestudante = estudante_id, dataHora = data_atual, tipo = 'DC3')
             if tarefa_check.exists():
                tarefa_obj = models.Tarefa.objects.get(fkestudante = estudante_id, dataHora = data_atual, tipo = 'DC3')
                if tarefa_obj.cumprida == 0:
                    tarefa_obj.cumprida = 1
                    tarefa_obj.save()
                    estudante_obj.pontuacao += 5 # estudante ganha 5 pontos por cumprir a tarefa
                    estudante_obj.save()
             #loop pra procurar tarefas do tipo postagem
            #  lista
             return Response(serializer.data)
class PostagemArmazenadaViewSet(viewsets.ModelViewSet):
    queryset = models.PostagemArmazenada.objects.all().order_by('dataHora')
    serializer_class = serializers.PostagemArmazenadaSerializer
    def create(self, request):
        serializer = serializers.PostagemArmazenadaSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            
            # data_request = request.data
            # print("\nId postagem:{}\n".format(data_request.get("id")))
            # print("\nrequest data:{}\n".format(data_request))
            # postArm = models.PostagemArmazenada.objects.get(id=)
            # print('\n query:{}\n'.format(data_request))
            # print('\n data de postagem:{}\n'.format(data_request["dataHora"]))
            if type(serializer.validated_data["dataHora"]) == type(None):
               serializer.validated_data["dataHora"] = django.utils.timezone.now()
            serializer.save()
        return Response(serializer.data)
    def list(self, request):
        #só postar se não for programada
        #caso contrario, precisa comparar o dia e hora 
        queryset = models.PostagemArmazenada.objects.all().order_by('dataHora')
        serializer = serializers.PostagemArmazenadaSerializer(queryset, many=True)
        data_send = serializer.data
        return_valid =[]
        if data_send != []:
            for obj_serializer in range(len(data_send)):
                date = data_send[obj_serializer]['dataHora'][:-6]
                print("\nrequest:{}\n".format(data_send))
                print("\nEsta sendo mandado:{}\n".format(date))
                # print("\nEsta sendo mandado:{}\n".format(data_send[0]['dataHora']))
                date_post = datetime.datetime.strptime(date,"%Y-%m-%dT%H:%M:%S")
                now = datetime.datetime.now()
                print("\nnow:{}\n".format(now))
                if date_post.date() <= now.date():
                    print("\ndate_post:{} e now:{}\n".format(date_post.date(),now.date()))
                    if date_post.time() <= now.time():
                        print("\ndate_post time:{} e now time:{}\n".format(date_post.time(),now.time()))
                        return_valid.append(data_send[obj_serializer])
                #             return Response(serializer.data,status=status.HTTP_200_OK)
                #         else:
                #             return Response([],status=status.HTTP_200_OK)
                #     else:
                #         return Response([])  
            return Response(return_valid,status=status.HTTP_200_OK)
        else:
            return Response(serializer.data)
class TarefaViewSet(viewsets.ModelViewSet):
    queryset = models.Tarefa.objects.all().order_by('dataHora')
    serializer_class = serializers.TarefaSerializer
    #post
    def create(self, request):
        serializer = serializers.TarefaSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            #salva os dados no banco
             serializer.save()
             #pega os dados que foram enviados pela requisição post
             data = request.data      

            #  lista
             return Response(serializer.data)

class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = models.Comentario.objects.all().order_by('dataHora')
    serializer_class = serializers.ComentarioSerializer
    #post
    def create(self, request):
        serializer = serializers.ComentarioSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            #salva os dados no banco
             serializer.save()
             #pega os dados que foram enviados pela requisição post
             data = request.data
             #pega o id correspondente à estudante que fez o post para poder acessar a pontuação
             estudante_id = data.get("fkestudante")
             estudante_obj = models.Estudante.objects.get(id=estudante_id)
             #atualizando a pontuação
             estudante_obj.pontuacao += 10
             estudante_obj.save()

             data_atual = datetime.date.today()
             tarefa_check = models.Tarefa.objects.filter(fkestudante = estudante_id, dataHora = data_atual, tipo = 'DC2')
             
             if tarefa_check.exists():
                tarefa_obj = models.Tarefa.objects.get(fkestudante = estudante_id, dataHora = data_atual, tipo = 'DC2')
                if tarefa_obj.cumprida == 0:
                    tarefa_obj.cumprida = 1
                    tarefa_obj.save()
                    estudante_obj.pontuacao += 5 # estudante ganha 5 pontos por cumprir a tarefa
                    estudante_obj.save()      

            #  lista
             return Response(serializer.data) 

#############Páginas que dependem de dados do banco###################
def home(request):
    response = requests.get('http://127.0.0.1:8000/postagem/')
    data = response.json()
    estudantes = [models.Estudante.objects.get(id=dict_est['fkusuario']).nome for dict_est in data ]
    #inserindo qual foi a estudante que realizoua postagem
    for post,i in zip(data,range(len(estudantes))):
        post['nome']=estudantes[i]
    return render(request, 'home.html', {'data': data})