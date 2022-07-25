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
# import json


# """"""Views"""""""
class PostagemViewSet(viewsets.ModelViewSet):
    queryset = models.Postagem.objects.all().order_by('-dataHora')
    serializer_class = serializers.PostagemSerializer
    #post
    def create(self, request):
        serializer = serializers.PostagemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
             #pega o ultimo usuario
             ultimo_usuario = list(models.Login.objects.all().order_by('id'))[-1].cpf
             serializer.validated_data['fkusuario'] = models.Estudante.objects.get(cpf=ultimo_usuario)
             serializer.validated_data['dataHora'] = django.utils.timezone.now()
             serializer.save()
             #####Estudante########
             #pega os dados que foram enviados pela requisição post
             data = serializer.validated_data
             #pega o id correspondente aestudante que fez o post para poder acessar a pontuação
             estudante_id = data["fkusuario"].id
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


             # atualizando o título
             titulo_atual = models.listaTitulo.objects.get(fkestudante = estudante_id, tituloAtual = 1)
             titulo_atual_obj = titulo_atual.fktitulo
             titulo_atual_nome = titulo_atual_obj.nome

             if estudante_obj.pontuacao > 840:
                if (estudante_obj.pontuacao <= 1680) and (titulo_atual_nome != 'Pontuação: 841 - 1680'):
                    titulo_atual.tituloAtual = 0
                    titulo_atual.save()
                    novo_titulo = models.Titulo.objects.get(nome = 'Pontuação: 841 - 1680')
                    novo_titulo_obj = models.listaTitulo.objects.create(fktitulo = novo_titulo, fkestudante = estudante_obj)
                    novo_titulo_obj.save()
                else:
                    if (estudante_obj.pontuacao > 1680) and (estudante_obj.pontuacao <= 3360) and (titulo_atual_nome != 'Pontuação: 1681 - 3360'):
                        titulo_atual.tituloAtual = 0
                        titulo_atual.save()
                        novo_titulo = models.Titulo.objects.get(nome = 'Pontuação: 1681 - 3360')
                        novo_titulo_obj = models.listaTitulo.objects.create(fktitulo = novo_titulo, fkestudante = estudante_obj)
                        novo_titulo_obj.save()
                    else:
                        if (estudante_obj.pontuacao > 3360) and (estudante_obj.pontuacao <= 6720) and (titulo_atual_nome != 'Pontuação: 3361 - 6720'):
                            titulo_atual.tituloAtual = 0
                            titulo_atual.save()
                            novo_titulo = models.Titulo.objects.get(nome = 'Pontuação: 3361 - 6720')
                            novo_titulo_obj = models.listaTitulo.objects.create(fktitulo = novo_titulo, fkestudante = estudante_obj)
                            novo_titulo_obj.save()
                        else:
                            if (estudante_obj.pontuacao > 6720) and (titulo_atual_nome != 'Pontuação: 6721 - oo'):
                                titulo_atual.tituloAtual = 0
                                titulo_atual.save()
                                novo_titulo = models.Titulo.objects.get(nome = 'Pontuação: 6721 - oo')
                                novo_titulo_obj = models.listaTitulo.objects.create(fktitulo = novo_titulo, fkestudante = estudante_obj)
                                novo_titulo_obj.save()                
             #loop pra procurar tarefas do tipo postagem
            #  lista
            #  return Response(serializer.data)
             return redirect("http://127.0.0.1:8000/home/")
class PostagemArmazenadaViewSet(viewsets.ModelViewSet):
    queryset = models.PostagemArmazenada.objects.all().order_by('-dataHora')
    serializer_class = serializers.PostagemArmazenadaSerializer
    def create(self, request):
        serializer = serializers.PostagemArmazenadaSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            #caso não seje informado a data e o horário que se deseja fazer a postagem, insere a data e horário presente
            if type(serializer.validated_data["dataHora"]) == type(None):
               serializer.validated_data["dataHora"] = django.utils.timezone.now()
            #pega o ultimo usuario
            ultimo_usuario = list(models.Login.objects.all().order_by('id'))[-1].cpf
            serializer.validated_data['fkusuario'] = models.Professor.objects.get(cpf=ultimo_usuario)
            serializer.save()
        # return Response(serializer.data)
        return redirect("http://127.0.0.1:8000/home/")
    def list(self, request):
        #precisa comparar o dia e hora 
        queryset = models.PostagemArmazenada.objects.all().order_by('-dataHora')
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
                        
            return Response(return_valid,status=status.HTTP_200_OK)
        else:
            return Response(serializer.data)
class TarefaViewSet(viewsets.ModelViewSet):
    queryset = models.Tarefa.objects.all().order_by('-dataHora')
    serializer_class = serializers.TarefaSerializer
    #post
    def create(self, request):
        serializer = serializers.TarefaSerializer(data=request.data)
        tarefas_todoMundo = []
        if serializer.is_valid(raise_exception=True):
            
            for estudante_obj in models.Estudante.objects.all():
                
                # serializer.validated_data["fkestudante"]=estudante_obj
                # print("\n Valor seriliazer:{}\n".format(serializer.validated_data))
                print("\n Valor seriliazer:{}\n".format(serializer.validated_data))
                tarefa_objeto = models.Tarefa.objects.create(
                                                            tipo=serializer.validated_data['tipo'],
                                                            dataHora = django.utils.timezone.now().date(),
                                                            fkestudante=estudante_obj
                                                            )
                
                tarefa_objeto.save()
                # serializer.save()
                # models.Tarefa.objects.create(texts=test)
            # for num_serilizer in tarefas_todoMundo:
            #     # models.Tarefa.objects.create(texts=test)
            #     print("\n Serializers:{}\n".format(num_serilizer))
            #     num_serilizer.save()
            return redirect("http://127.0.0.1:8000/home/")
            # #salva os dados no banco
            #  serializer.save()
            #  #pega os dados que foram enviados pela requisição post
            #  data = request.data      

            # #  lista
            # #  return Response(serializer.data)
            #  return redirect("http://127.0.0.1:8000/home/")

class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = models.Comentario.objects.all().order_by('-dataHora')
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

             # atualizando o título
             titulo_atual = models.listaTitulo.objects.get(fkestudante = estudante_id, tituloAtual = 1)
             titulo_atual_obj = titulo_atual.fktitulo
             titulo_atual_nome = titulo_atual_obj.nome

             if estudante_obj.pontuacao > 840:
                if (estudante_obj.pontuacao <= 1680) and (titulo_atual_nome != 'Pontuação: 841 - 1680'):
                    titulo_atual.tituloAtual = 0
                    titulo_atual.save()
                    novo_titulo = models.Titulo.objects.get(nome = 'Pontuação: 841 - 1680')
                    novo_titulo_obj = models.listaTitulo.objects.create(fktitulo = novo_titulo, fkestudante = estudante_obj)
                    novo_titulo_obj.save()
                else:
                    if (estudante_obj.pontuacao > 1680) and (estudante_obj.pontuacao <= 3360) and (titulo_atual_nome != 'Pontuação: 1681 - 3360'):
                        titulo_atual.tituloAtual = 0
                        titulo_atual.save()
                        novo_titulo = models.Titulo.objects.get(nome = 'Pontuação: 1681 - 3360')
                        novo_titulo_obj = models.listaTitulo.objects.create(fktitulo = novo_titulo, fkestudante = estudante_obj)
                        novo_titulo_obj.save()
                    else:
                        if (estudante_obj.pontuacao > 3360) and (estudante_obj.pontuacao <= 6720) and (titulo_atual_nome != 'Pontuação: 3361 - 6720'):
                            titulo_atual.tituloAtual = 0
                            titulo_atual.save()
                            novo_titulo = models.Titulo.objects.get(nome = 'Pontuação: 3361 - 6720')
                            novo_titulo_obj = models.listaTitulo.objects.create(fktitulo = novo_titulo, fkestudante = estudante_obj)
                            novo_titulo_obj.save()
                        else:
                            if (estudante_obj.pontuacao > 6720) and (titulo_atual_nome != 'Pontuação: 6721 - oo'):
                                titulo_atual.tituloAtual = 0
                                titulo_atual.save()
                                novo_titulo = models.Titulo.objects.get(nome = 'Pontuação: 6721 - oo')
                                novo_titulo_obj = models.listaTitulo.objects.create(fktitulo = novo_titulo, fkestudante = estudante_obj)
                                novo_titulo_obj.save()              

            #  lista
            #  return Response(serializer.data)
             return redirect("http://127.0.0.1:8000/home/")

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
                    return redirect("http://127.0.0.1:8000/home/")
                else:
                    serializer.validated_data["eh_usuario"] = False
                    serializer.validated_data["dataHora"] = django.utils.timezone.now()
                    serializer.save()
                    
                    return redirect("http://127.0.0.1:8000/?erro=cpf_invalido")

class RankingViewSet(viewsets.ModelViewSet):
    #queryset = models.Login.objects.all()
    #serializer_class = serializers.LoginSerializer
    queryset = models.Estudante.objects.all().order_by('-pontuacao')
    serializer_class = serializers.RankingSerializer
    http_method_names = ['get', 'head', 'options']

    def list(self,request):
        #ordenar os alunos por ponto
        #retorna uma lista de alunos
        #serializer = serializers.LoginSerializer(data=request.data)
        queryset = models.Estudante.objects.all().order_by('-pontuacao')
        serializer =  serializers.RankingSerializer(queryset,many=True)

        ranking = models.Estudante.objects.all().order_by('-pontuacao').values_list('nome', 'pontuacao')
        return Response(list(ranking))
   

class ProfessorViewSet(viewsets.ModelViewSet):    
    queryset = models.Professor.objects.all().order_by('nome')
    serializer_class = serializers.ProfessorSerializer

    def list(self,request):
        queryset = models.Professor.objects.all().order_by('nome')
        serializer =  serializers.ProfessorSerializer(queryset,many=True)
        professoras = models.Professor.objects.all().order_by('nome').values_list('nome')
        return Response(list(professoras))

class criaTituloViewSet(viewsets.ModelViewSet):    
    queryset = models.Titulo.objects.all()
    serializer_class = serializers.criaTituloSerializer

    def create(self, request):
        serializer = serializers.criaTituloSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            #salva os dados no banco
             serializer.save()
             #pega os dados que foram enviados pela requisição post
             data = request.data      

            #  lista
             return Response(serializer.data)

class UsuarioViewSet(viewsets.ModelViewSet):    
    queryset = models.Professor.objects.order_by('nome')
    serializer_class = serializers.ProfessorSerializer

    #queryset = models.Estudante.objects.order_by('nome')
    #serializer_class = serializers.EstudanteSerializer

    def list(self,request):
        queryset = models.Professor.objects.order_by('nome')
        serializer_class = serializers.ProfessorSerializer(queryset,many=True)
        professoras = models.Professor.objects.order_by('nome').values_list('nome')
        alunas = models.Estudante.objects.order_by('nome').values_list('nome')

        usuarios = list(professoras) + list(alunas)
        usuarios.sort()
        
        return Response(usuarios)
    
  
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
    response_user= requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]

    data_aluna = response_aluna.json()
    data_prof = response_prof.json()
    
    estudantes = [models.Estudante.objects.get(id=dict_est['fkusuario']).nome for dict_est in data_aluna ]
    professora = [models.Professor.objects.get(id=dict_est['fkusuario']).nome for dict_est in data_prof ]
    
    #identificar se é uma aluna que está logada
    eh_estudante =  models.Estudante.objects.filter(cpf = user_ultimo["cpf"])
    c={}
    if eh_estudante.exists():
        c['nao_aluna'] = False
    else:
        c['nao_aluna'] = True

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
    return render(request, 'home.html', {'data': data,'c':c})

@csrf_protect 
def login(request):
    c = {'erro_message':request.GET.get('erro','')}
    if c['erro_message']!="":
        c['is_erro']=True
    else:
        c['is_erro']=False
    return render(request,'login.html',c)

#informações sobre título atual
def tituloAtual(request):
    response_user= requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]
    eh_estudante =  models.Estudante.objects.filter(cpf = user_ultimo["cpf"])
    print("\n Aluna objeto:{}\n".format(eh_estudante))
    if eh_estudante.exists():
        list_titulos = models.listaTitulo.objects.filter(fkestudante=list(eh_estudante)[0]).order_by('-dataHora')
        print("\n Lista de Títulos de uma aluna:{}\n".format(list_titulos))
        #pega o titulo mais novo
        lista = list_titulos[0]
        obj_titulo_atual = lista.fktitulo
        pega_titulo = models.Titulo.objects.get(id=obj_titulo_atual.id).desc
        print("\n Aluna:{} \n Titulo atual:{}\n".format(list(eh_estudante)[0].nome,pega_titulo))
        
        #pegando as informações sobre pontos do próximo título
        prox_titulo_id = lista.fktitulo.id + 1 
        titulo_prox = models.Titulo.objects.get(id=prox_titulo_id)
        qtdPontos_prox = titulo_prox.qtdPontos

        #nomes dos títulos que a aluna já teve
        nomes_titulos = [models.Titulo.objects.get(id = listTitulo.fktitulo_id).desc for listTitulo in list_titulos]
        c = {
            'aluna': {
                'nome': list(eh_estudante)[0].nome,
                'titulo': pega_titulo,
                'pontuacao': list(eh_estudante)[0].pontuacao,
                'pontos_para_prox_titulo': qtdPontos_prox - list(eh_estudante)[0].pontuacao,
            },
            'historico': [ {'titulo':nomeTitulo, 'data': dateTime.dataHora} for nomeTitulo,dateTime in zip(nomes_titulos,list_titulos)
                # {'titulo': "Nome do titulo 1", 'data': '21/07/2022'},
                # {'titulo': "Nome do titulo 2", 'data': '22/07/2022'},
                # {'titulo': "Nome do titulo 3", 'data': '23/07/2022'},
                # {'titulo': "Nome do titulo 4", 'data': '24/07/2022'},
                # {'titulo': "Nome do titulo 5", 'data': '25/07/2022'}
            ]
        }
        c['nao_aluna'] = False
        return render(request,'tituloAtual.html', c)
        # print(list(eh_estudante)[0].id)
        # c={'id_user':list(eh_estudante)[0].id}
        # return render(request,'tituloAtual.html', )
    else:
        c = {'nao_aluna':True}
        return render(request,'home.html',c)

# Elencar todos os usuários
def listarTodosUsuarios(request):
    response_user= requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]
    eh_estudante =  models.Estudante.objects.filter(cpf = user_ultimo["cpf"])
    print("\n Aluna objeto:{}\n".format(eh_estudante))
    if eh_estudante.exists():
        list_usuarios = models.Estudante.objects.order_by('nome')
        list_listaTitulo=[]
        for usuario in list_usuarios:
            list_listaTitulo.append(models.listaTitulo.objects.filter(fkestudante=usuario).order_by('-dataHora')[0].fktitulo_id)
        print("\n Aluna:{} \n Pontuacao:{}\n".format(list(list_usuarios)[0].nome,list(list_usuarios)[0].pontuacao))
        listaAlunas = []
        
        for nomeAluna,id_titulo in zip(list_usuarios,list_listaTitulo):
            listaAlunas.append({'nome': nomeAluna.nome,'pontos': nomeAluna.pontuacao,'titulo':models.Titulo.objects.get(id=id_titulo).desc})
        
        c = {
            'usuarios': listaAlunas
        }
        c['nao_aluna'] = False
        return render(request,'usuarios.html', c)
        # print(list(eh_estudante)[0].id)
        # c={'id_user':list(eh_estudante)[0].id}
        # return render(request,'tituloAtual.html', )
    else:
        c = {'nao_aluna':True}
        return render(request,'home.html',c)

# Elencar todos os usuários com o mesmo titulo
def listarUsuariosMesmoTitulo(request):
    response_user= requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]
    eh_estudante =  models.Estudante.objects.filter(cpf = user_ultimo["cpf"])
    print("\n Aluna objeto:{}\n".format(eh_estudante))
    if eh_estudante.exists():
        list_usuarios = models.Estudante.objects.all().order_by('nome')
        tituloSerMostrado_id = models.listaTitulo.objects.filter(fkestudante_id=list(eh_estudante)[0].id).order_by('-dataHora')[0].fktitulo_id
        nomeTituloSerMostrado = models.Titulo.objects.filter(id=tituloSerMostrado_id)[0].desc
        list_UsuariosMesmoTitulo=[]
        for usuario in list_usuarios:
            print(models.listaTitulo.objects.filter(fkestudante=usuario).order_by('-dataHora'))
            if tituloSerMostrado_id==list(models.listaTitulo.objects.filter(fkestudante=usuario).order_by('-dataHora'))[0].fktitulo_id:
                list_UsuariosMesmoTitulo.append(models.listaTitulo.objects.filter(fkestudante=usuario).order_by('-dataHora')[0].fktitulo_id)
        print("\n Aluna:{} \n Pontuacao:{}\n".format(list(list_usuarios)[0].nome,list(list_usuarios)[0].pontuacao))
        listaAlunas = []
        
        for nomeAluna in list_usuarios:
            listaAlunas.append({'nome': nomeAluna.nome,'pontos': nomeAluna.pontuacao})
        
        c = {
            'usuarios': listaAlunas
        }
        c['nao_aluna'] = False
        return render(request,'usuariosMesmoTitulo.html', c)
        # print(list(eh_estudante)[0].id)
        # c={'id_user':list(eh_estudante)[0].id}
        # return render(request,'tituloAtual.html', )
    else:
        c = {'nao_aluna':True}
        return render(request,'home.html',c)

# Elencar todos os usuários com o mesmo titulo
def ranking(request):
    response_user= requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]
    eh_estudante =  models.Estudante.objects.filter(cpf = user_ultimo["cpf"])
    print("\n Aluna objeto:{}\n".format(eh_estudante))
    if eh_estudante.exists():
        list_usuarios = models.Estudante.objects.all().order_by('-pontuacao')
        listaAlunas = []
        
        for nomeAluna in list_usuarios:
            listaAlunas.append({'nome': nomeAluna.nome,'pontos': nomeAluna.pontuacao})
        
        c = {
            'usuarios': listaAlunas
        }
        c['nao_aluna'] = False
        return render(request,'ranking.html', c)
        # print(list(eh_estudante)[0].id)
        # c={'id_user':list(eh_estudante)[0].id}
        # return render(request,'tituloAtual.html', )
    else:
        c = {'nao_aluna':True}
        return render(request,'home.html',c)

@csrf_protect 
def criarPost(request):
    response_user= requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]
    # estudantes = [models.Estudante.objects.get(id=dict_est['fkusuario']).nome for dict_est in data_aluna ]
    eh_estudante =  models.Estudante.objects.filter(cpf = user_ultimo["cpf"])
    eh_professor =  models.Professor.objects.filter(cpf = user_ultimo["cpf"])
    if eh_estudante.exists():
        print(list(eh_estudante)[0].id)
        c={'id_user':list(eh_estudante)[0].id}
        c['nao_aluna']=False
        return render(request,'criarPost.html',c)
    elif eh_professor.exists():
        c={'id_user':list(eh_professor)[0].id}
        c['nao_aluna']=True
        return render(request,'criarPost_professora.html', c)


# def visualizacao(request):
    # print('display functio')
    # d=upload.objects.last()
    # test=sr.takeCommand(d.file.path)
    # # will store the record in the database
    # p = text.objects.create(texts=test)
    # print(test)
    # return render(request,'thanks.html',{'print':test})
################Páginas estáticas################
#página estática de títulos
def titulos(request):
    response_user= requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]
    eh_estudante =  models.Estudante.objects.filter(cpf = user_ultimo["cpf"])
    c={}
    if eh_estudante.exists():
        c['nao_aluna'] = False
    else:
        c['nao_aluna'] = True
    return render(request,'titulos.html',c)

def tutorial(request):
    response_user= requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]
    eh_estudante =  models.Estudante.objects.filter(cpf = user_ultimo["cpf"])
    c={}
    if eh_estudante.exists():
        c['nao_aluna'] = False
    else:
        c['nao_aluna'] = True
    return render(request,'tutorial.html',c)

def sobre(request):
    response_user= requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]
    eh_estudante =  models.Estudante.objects.filter(cpf = user_ultimo["cpf"])
    c={}
    if eh_estudante.exists():
        c['nao_aluna'] = False
    else:
        c['nao_aluna'] = True
    return render(request,'sobre.html',c)

def politicas(request):
    response_user= requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]
    eh_estudante =  models.Estudante.objects.filter(cpf = user_ultimo["cpf"])
    c={}
    if eh_estudante.exists():
        c['nao_aluna'] = False
    else:
        c['nao_aluna'] = True
    return render(request,'politicas.html',c)

def assistencia(request):
    response_user= requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]
    eh_estudante =  models.Estudante.objects.filter(cpf = user_ultimo["cpf"])
    c={}
    if eh_estudante.exists():
        c['nao_aluna'] = False
    else:
        c['nao_aluna'] = True
    return render(request,'assistenciaEstudantil.html',c)

def professoras(request):
    response_user= requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]
    eh_estudante =  models.Estudante.objects.filter(cpf = user_ultimo["cpf"])
    c={}
    if eh_estudante.exists():
        c['nao_aluna'] = False
    else:
        c['nao_aluna'] = True
    return render(request,'professoras.html',c)
