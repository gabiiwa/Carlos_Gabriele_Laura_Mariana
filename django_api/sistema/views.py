# from asyncio.windows_events import NULL
from urllib import response
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from rest_framework import viewsets,status
from sistema import serializers
from sistema import models
from rest_framework.response import Response
import requests
import datetime
from django.http import JsonResponse
import django
import json


# """"""Views"""""""
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

             data_atual = django.utils.timezone.now()
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
            #caso não seje informado a data e o horário que se deseja fazer a postagem, insere a data e horário presente
            if type(serializer.validated_data["dataHora"]) == type(None):
               serializer.validated_data["dataHora"] = django.utils.timezone.now()
            serializer.save()
        return Response(serializer.data)
    def list(self, request):
        #precisa comparar o dia e hora 
        queryset = models.PostagemArmazenada.objects.all().order_by('dataHora')
        serializer = serializers.PostagemArmazenadaSerializer(queryset, many=True)
        data_send = serializer.data
        #guarda as postagens que a data de postagem for menor que a data atual
        return_valid =[]
        #caso não tenha postagem feita ainda, o serializer estará vazio
        if data_send != []:
            #itera em todas postagens no banco
            for obj_serializer in range(len(data_send)):
                date = data_send[obj_serializer]['dataHora'][:19]
                #transforma a data de str para o formato datetime
                date_post = datetime.datetime.strptime(date,"%Y-%m-%dT%H:%M:%S")
                #pega a data e o horário atual
                now = datetime.datetime.now()
                #se a data e o horário programado de postagem já chegou, este é guardado pro return
                if date_post.date() <= now.date():
                    if date_post.time() <= now.time():
                        return_valid.append(data_send[obj_serializer])
                        
            # print("\n Socorrro, esse é a saida de postagem programada:{}\n".format(return_valid))
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

             data_atual = django.utils.timezone.now()
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

class LoginViewSet(viewsets.ModelViewSet):
    queryset = models.Login.objects.all()
    serializer_class = serializers.LoginSerializer
    
    def create(self,request):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if type(serializer.validated_data) != type(None):
                estudante = models.Estudante.objects.filter(cpf = serializer.validated_data["cpf"])
                professora = models.Professor.objects.filter(cpf = serializer.validated_data["cpf"])
                if estudante.exists() or professora.exists():
                    serializer.validated_data["eh_usuario"] = True
                    serializer.validated_data["dataHora"] = django.utils.timezone.now()
                    serializer.save()
                    # redirect("home/")
                    # return Response(serializer.data)
                    return redirect("http://127.0.0.1:8000/home/")
                else:
                    serializer.validated_data["eh_usuario"] = False
                    serializer.validated_data["dataHora"] = django.utils.timezone.now()
                    serializer.save()
                    # redirect("http://127.0.0.1:8000/",{'erro':'cpf invalido'})
                    # return JsonResponse({'erro':'cpf invalido'})
                    return redirect("http://127.0.0.1:8000/?erro=cpf_invalido")

class EstudanteViewSet(viewsets.ModelViewSet):
    queryset = models.Login.objects.all()
    serializer_class = serializers.LoginSerializer
    def ranking(self,request):
        #ordenar os alunos por ponto
        #retorna uma lista de alunos
        return
    
  
class VisualizacaoViewSet(viewsets.ModelViewSet):
    # foiVisualizado = models.BooleanField(default=False)
    # ehPontoExtra = models.BooleanField(default=False)
    # qtdPontos = models.IntegerField()
    # fkpostagem = models.ForeignKey(Postagem,on_delete=models.CASCADE, blank=True, null=True)
    # fkprogramada = models.ForeignKey(PostagemArmazenada,on_delete=models.CASCADE, blank=True, null=True) 
    queryset = models.Visualizacao.objects.all()
    serializer_class = serializers.VisualizacaoSerializer

#############Páginas que dependem de dados do banco###################
def home(request):
    response_aluna = requests.get('http://127.0.0.1:8000/router/postagem/')
    response_prof = requests.get('http://127.0.0.1:8000/router/postagem_armazenada/')

    data_aluna = response_aluna.json()
    data_prof = response_prof.json()
    
    estudantes = [models.Estudante.objects.get(id=dict_est['fkusuario']).nome for dict_est in data_aluna ]
    professora = [models.Professor.objects.get(id=dict_est['fkusuario']).nome for dict_est in data_prof ]
    
   #inserindo qual foi a estudante que realizoua postagem
    for post,i in zip(data_aluna,range(len(estudantes))):
        post['nome']=estudantes[i]
        date = models.Postagem.objects.get(id=post['fkusuario']).dataHora
        #transforma a data de str para o formato datetime
        post['dataHora']=date
    data = data_aluna
    for post,i in zip(data_prof,range(len(professora))):
        post['nome']=professora[i]
        date = models.PostagemArmazenada.objects.get(id=post['fkusuario']).dataHora
        #transforma a data de str para o formato datetime
        post['dataHora']=date
    data = data + data_prof
    return render(request, 'home.html', {'data': data})

@csrf_protect 
def login(request):
    # c={'verifica':False,'id_user':0}
    # response = requests.get('http://127.0.0.1:8000/router/login/')
    # response_login = requests.get('http://127.0.0.1:8000')
    # data = response.json()
    # print(response_login.json())
    # print(request.GET.get('erro',''))
    # print(response.json())
    
    # eh_usuario = ultimo_user["eh_usuario"]
    # usuario_id = ultimo_user["cpf"]
    # c = {'verifica':eh_usuario,'id_user':usuario_id}
    # if eh_usuario==False:
    c = {'erro_message':request.GET.get('erro','')}
    if c['erro_message']!="":
        c['is_erro']=True
    else:
        c['is_erro']=False
    print("\nc:{}\n".format(c))
    return render(request,'login.html',c)


