# from asyncio.windows_events import NULL
# from asyncio.windows_events import NULL
from urllib import response
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from rest_framework import viewsets, status
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
    # post

    def create(self, request):
        serializer = serializers.PostagemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # pega o ultimo usuario
            ultimo_usuario = list(
                models.Login.objects.all().order_by('id'))[-1].cpf
            serializer.validated_data['fkusuario'] = models.Estudante.objects.get(
                cpf=ultimo_usuario)
            serializer.validated_data['dataHora'] = django.utils.timezone.now()
            serializer.save()
            #####Estudante########
            # pega os dados que foram enviados pela requisição post
            data = serializer.validated_data
            # pega o id correspondente aestudante que fez o post para poder acessar a pontuação
            estudante_id = data["fkusuario"].id
            estudante_obj = models.Estudante.objects.get(id=estudante_id)
            # atualizando a pontuação
            estudante_obj.pontuacao += 15
            estudante_obj.save()

            data_atual = django.utils.timezone.now()
            tarefa_check = models.Tarefa.objects.filter(
                fkestudante=estudante_id, dataHora=data_atual, tipo='DC3')
            if tarefa_check.exists():
                tarefa_obj = models.Tarefa.objects.get(
                    fkestudante=estudante_id, dataHora=data_atual, tipo='DC3')
                if tarefa_obj.cumprida == 0:
                    tarefa_obj.cumprida = 1
                    tarefa_obj.save()
                    estudante_obj.pontuacao += 5  # estudante ganha 5 pontos por cumprir a tarefa
                    estudante_obj.save()

            # atualizando o título
            titulo_atual = models.listaTitulo.objects.get(
                fkestudante=estudante_id, tituloAtual=1)
            titulo_atual_obj = titulo_atual.fktitulo
            titulo_atual_nome = titulo_atual_obj.nome

            if estudante_obj.pontuacao > 840:
                if (estudante_obj.pontuacao <= 1680) and (titulo_atual_nome != 'Pontuação: 841 - 1680'):
                    titulo_atual.tituloAtual = 0
                    titulo_atual.save()
                    novo_titulo = models.Titulo.objects.get(
                        nome='Pontuação: 841 - 1680')
                    novo_titulo_obj = models.listaTitulo.objects.create(
                        fktitulo=novo_titulo, fkestudante=estudante_obj)
                    novo_titulo_obj.save()
                else:
                    if (estudante_obj.pontuacao > 1680) and (estudante_obj.pontuacao <= 3360) and (titulo_atual_nome != 'Pontuação: 1681 - 3360'):
                        titulo_atual.tituloAtual = 0
                        titulo_atual.save()
                        novo_titulo = models.Titulo.objects.get(
                            nome='Pontuação: 1681 - 3360')
                        novo_titulo_obj = models.listaTitulo.objects.create(
                            fktitulo=novo_titulo, fkestudante=estudante_obj)
                        novo_titulo_obj.save()
                    else:
                        if (estudante_obj.pontuacao > 3360) and (estudante_obj.pontuacao <= 6720) and (titulo_atual_nome != 'Pontuação: 3361 - 6720'):
                            titulo_atual.tituloAtual = 0
                            titulo_atual.save()
                            novo_titulo = models.Titulo.objects.get(
                                nome='Pontuação: 3361 - 6720')
                            novo_titulo_obj = models.listaTitulo.objects.create(
                                fktitulo=novo_titulo, fkestudante=estudante_obj)
                            novo_titulo_obj.save()
                        else:
                            if (estudante_obj.pontuacao > 6720) and (titulo_atual_nome != 'Pontuação: 6721 - oo'):
                                titulo_atual.tituloAtual = 0
                                titulo_atual.save()
                                novo_titulo = models.Titulo.objects.get(
                                    nome='Pontuação: 6721 - oo')
                                novo_titulo_obj = models.listaTitulo.objects.create(
                                    fktitulo=novo_titulo, fkestudante=estudante_obj)
                                novo_titulo_obj.save()

            #  if models.Estudante.objects.get(id=1):
            #     for i in range(56):
            #         postagem_create = models.Postagem.objects.create(titulo="Mudar de título {}".format(i),
            #                                                         texto="quantidade de texto necessária para mudar de título",
            #                                                         fkusuario=models.Estudante.objects.get(id=1),
            #                                                         dataHora = django.utils.timezone.now())
            #         postagem_create.save()
            #         #atualizando a pontuação
            #         estudante_obj.pontuacao += 15
            #         estudante_obj.save()

            #         data_atual = django.utils.timezone.now()
            #         tarefa_check = models.Tarefa.objects.filter(fkestudante = estudante_id, dataHora = data_atual, tipo = 'DC3')
            #         if tarefa_check.exists():
            #             tarefa_obj = models.Tarefa.objects.get(fkestudante = estudante_id, dataHora = data_atual, tipo = 'DC3')
            #             if tarefa_obj.cumprida == 0:
            #                 tarefa_obj.cumprida = 1
            #                 tarefa_obj.save()
            #                 estudante_obj.pontuacao += 5 # estudante ganha 5 pontos por cumprir a tarefa
            #                 estudante_obj.save()

            #         # atualizando o título
            #         titulo_atual = models.listaTitulo.objects.get(fkestudante = estudante_id, tituloAtual = 1)
            #         titulo_atual_obj = titulo_atual.fktitulo
            #         titulo_atual_nome = titulo_atual_obj.nome

            #         if estudante_obj.pontuacao > 840:
            #             if (estudante_obj.pontuacao <= 1680) and (titulo_atual_nome != 'Pontuação: 841 - 1680'):
            #                 titulo_atual.tituloAtual = 0
            #                 titulo_atual.save()
            #                 novo_titulo = models.Titulo.objects.get(nome = 'Pontuação: 841 - 1680')
            #                 novo_titulo_obj = models.listaTitulo.objects.create(fktitulo = novo_titulo, fkestudante = estudante_obj)
            #                 novo_titulo_obj.save()
            #             else:
            #                 if (estudante_obj.pontuacao > 1680) and (estudante_obj.pontuacao <= 3360) and (titulo_atual_nome != 'Pontuação: 1681 - 3360'):
            #                     titulo_atual.tituloAtual = 0
            #                     titulo_atual.save()
            #                     novo_titulo = models.Titulo.objects.get(nome = 'Pontuação: 1681 - 3360')
            #                     novo_titulo_obj = models.listaTitulo.objects.create(fktitulo = novo_titulo, fkestudante = estudante_obj)
            #                     novo_titulo_obj.save()
            #                 else:
            #                     if (estudante_obj.pontuacao > 3360) and (estudante_obj.pontuacao <= 6720) and (titulo_atual_nome != 'Pontuação: 3361 - 6720'):
            #                         titulo_atual.tituloAtual = 0
            #                         titulo_atual.save()
            #                         novo_titulo = models.Titulo.objects.get(nome = 'Pontuação: 3361 - 6720')
            #                         novo_titulo_obj = models.listaTitulo.objects.create(fktitulo = novo_titulo, fkestudante = estudante_obj)
            #                         novo_titulo_obj.save()
            #                     else:
            #                         if (estudante_obj.pontuacao > 6720) and (titulo_atual_nome != 'Pontuação: 6721 - oo'):
            #                             titulo_atual.tituloAtual = 0
            #                             titulo_atual.save()
            #                             novo_titulo = models.Titulo.objects.get(nome = 'Pontuação: 6721 - oo')
            #                             novo_titulo_obj = models.listaTitulo.objects.create(fktitulo = novo_titulo, fkestudante = estudante_obj)
            #                             novo_titulo_obj.save()
            return redirect("http://127.0.0.1:8000/home/")


class PostagemArmazenadaViewSet(viewsets.ModelViewSet):
    queryset = models.PostagemArmazenada.objects.all().order_by('-dataHora')
    serializer_class = serializers.PostagemArmazenadaSerializer

    def create(self, request):
        serializer = serializers.PostagemArmazenadaSerializer(
            data=request.data)
        if serializer.is_valid(raise_exception=True):
            # caso não seje informado a data e o horário que se deseja fazer a postagem, insere a data e horário presente
            if type(serializer.validated_data["dataHora"]) == type(None):
                serializer.validated_data["dataHora"] = django.utils.timezone.now(
                )
            # pega o ultimo usuario
            ultimo_usuario = list(
                models.Login.objects.all().order_by('id'))[-1].cpf
            serializer.validated_data['fkusuario'] = models.Professor.objects.get(
                cpf=ultimo_usuario)
            serializer.save()
        # return Response(serializer.data)
        return redirect("http://127.0.0.1:8000/home/")

    def list(self, request):
        # precisa comparar o dia e hora
        queryset = models.PostagemArmazenada.objects.all().order_by('-dataHora')
        serializer = serializers.PostagemArmazenadaSerializer(
            queryset, many=True)
        data_send = serializer.data
        # guarda as postagens que a data de postagem for menor que a data atual
        return_valid = []
        # caso não tenha postagem feita ainda, o serializer estará vazio
        if data_send != []:
            # itera em todas postagens no banco
            for obj_serializer in range(len(data_send)):
                date = data_send[obj_serializer]['dataHora'][:19]
                # transforma a data de str para o formato datetime
                date_post = datetime.datetime.strptime(
                    date, "%Y-%m-%dT%H:%M:%S")
                # pega a data e o horário atual
                now = datetime.datetime.now()
                # se a data e o horário programado de postagem já chegou, este é guardado pro return
                if date_post.date() <= now.date():
                    if date_post.time() <= now.time():
                        return_valid.append(data_send[obj_serializer])

            return Response(return_valid, status=status.HTTP_200_OK)
        else:
            return Response(serializer.data)


class TarefaViewSet(viewsets.ModelViewSet):
    queryset = models.Tarefa.objects.all().order_by('-dataHora')
    serializer_class = serializers.TarefaSerializer
    # post

    def create(self, request):
        serializer = serializers.TarefaSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            print("\n Valor seriliazer:{}\n".format(serializer.validated_data))
            if models.Tarefa.objects.filter(dataHora=django.utils.timezone.now().date()).exists()==False:
                for estudante_obj in list(models.Estudante.objects.all()):
                    print("\n Estudante:{}\n".format(estudante_obj))
                    tarefa_objeto = models.Tarefa.objects.create(
                        tipo=serializer.validated_data['tipo'],
                        dataHora=django.utils.timezone.now().date(),
                        fkestudante=estudante_obj
                    )

                    tarefa_objeto.save()

            return redirect("http://127.0.0.1:8000/home/")


class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = models.Comentario.objects.all().order_by('-dataHora')
    serializer_class = serializers.ComentarioSerializer
    # post

    def create(self, request):
        serializer = serializers.ComentarioSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
             
            #pega os dados que foram enviados pela requisição post
            data = request.data
            #pegando ultimo usuario
            ultimo_cpf = (list(models.Login.objects.all())[-1].cpf,)
            cpf_estudantes = list(models.Estudante.objects.all().values_list('cpf'))
            print("\n ultimo cpf:{} \n Cpf alunas:{}\n".format(ultimo_cpf,cpf_estudantes))

            
            if ultimo_cpf in cpf_estudantes:
                # pega o id correspondente à estudante que fez o post para poder acessar a pontuação
                estudante_id = data.get("fkestudante")
                estudante_obj = models.Estudante.objects.get(id=estudante_id)
                # atualizando a pontuação
                estudante_obj.pontuacao += 10
                estudante_obj.save()

                data_atual = django.utils.timezone.now()
                tarefa_check = models.Tarefa.objects.filter(
                    fkestudante=estudante_id, dataHora=data_atual, tipo='DC2')

                if tarefa_check.exists():
                    tarefa_obj = models.Tarefa.objects.get(
                        fkestudante=estudante_id, dataHora=data_atual, tipo='DC2')
                    if tarefa_obj.cumprida == 0:
                        tarefa_obj.cumprida = 1
                        tarefa_obj.save()
                        estudante_obj.pontuacao += 5  # estudante ganha 5 pontos por cumprir a tarefa
                        estudante_obj.save()

                # atualizando o título
                titulo_atual = models.listaTitulo.objects.get(
                    fkestudante=estudante_id, tituloAtual=1)
                titulo_atual_obj = titulo_atual.fktitulo
                titulo_atual_nome = titulo_atual_obj.nome

                if estudante_obj.pontuacao > 840:
                    if (estudante_obj.pontuacao <= 1680) and (titulo_atual_nome != 'Pontuação: 841 - 1680'):
                        titulo_atual.tituloAtual = 0
                        titulo_atual.save()
                        novo_titulo = models.Titulo.objects.get(
                            nome='Pontuação: 841 - 1680')
                        novo_titulo_obj = models.listaTitulo.objects.create(
                            fktitulo=novo_titulo, fkestudante=estudante_obj)
                        novo_titulo_obj.save()
                    else:
                        if (estudante_obj.pontuacao > 1680) and (estudante_obj.pontuacao <= 3360) and (titulo_atual_nome != 'Pontuação: 1681 - 3360'):
                            titulo_atual.tituloAtual = 0
                            titulo_atual.save()
                            novo_titulo = models.Titulo.objects.get(
                                nome='Pontuação: 1681 - 3360')
                            novo_titulo_obj = models.listaTitulo.objects.create(
                                fktitulo=novo_titulo, fkestudante=estudante_obj)
                            novo_titulo_obj.save()
                        else:
                            if (estudante_obj.pontuacao > 3360) and (estudante_obj.pontuacao <= 6720) and (titulo_atual_nome != 'Pontuação: 3361 - 6720'):
                                titulo_atual.tituloAtual = 0
                                titulo_atual.save()
                                novo_titulo = models.Titulo.objects.get(
                                    nome='Pontuação: 3361 - 6720')
                                novo_titulo_obj = models.listaTitulo.objects.create(
                                    fktitulo=novo_titulo, fkestudante=estudante_obj)
                                novo_titulo_obj.save()
                            else:
                                if (estudante_obj.pontuacao > 6720) and (titulo_atual_nome != 'Pontuação: 6721 - oo'):
                                    titulo_atual.tituloAtual = 0
                                    titulo_atual.save()
                                    novo_titulo = models.Titulo.objects.get(
                                        nome='Pontuação: 6721 - oo')
                                    novo_titulo_obj = models.listaTitulo.objects.create(
                                        fktitulo=novo_titulo, fkestudante=estudante_obj)
                                    novo_titulo_obj.save()
                else:
                    serializer.validated_data["fkprofessor"] = models.Professor.objects.get(
                        cpf=ultimo_cpf)

            #  lista
            #  return Response(serializer.data)
            # salva os dados no banco
            serializer.save()
            return redirect("http://127.0.0.1:8000/home/")


class LoginViewSet(viewsets.ModelViewSet):
    queryset = models.Login.objects.all()
    serializer_class = serializers.LoginSerializer

    def create(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if type(serializer.validated_data) != type(None):
                estudante = models.Estudante.objects.filter(
                    cpf=serializer.validated_data["cpf"])
                professora = models.Professor.objects.filter(
                    cpf=serializer.validated_data["cpf"])

                if estudante.exists() or professora.exists():
                    serializer.validated_data["eh_usuario"] = True
                    serializer.validated_data["dataHora"] = django.utils.timezone.now(
                    )
                    serializer.save()
                    return redirect("http://127.0.0.1:8000/home/")
                else:
                    serializer.validated_data["eh_usuario"] = False
                    serializer.validated_data["dataHora"] = django.utils.timezone.now(
                    )
                    serializer.save()

                    return redirect("http://127.0.0.1:8000/?erro=cpf_invalido")


class RankingViewSet(viewsets.ModelViewSet):
    #queryset = models.Login.objects.all()
    #serializer_class = serializers.LoginSerializermodels.PostagemArmazenada.objects.filter(fkusuario_id=id_usuario,id=id_postagem)
    queryset = models.Estudante.objects.all().order_by('-pontuacao')
    serializer_class = serializers.RankingSerializer
    http_method_names = ['get', 'head', 'options']

    def list(self, request):
        # ordenar os alunos por ponto
        # retorna uma lista de alunos
        queryset = models.Estudante.objects.all().order_by('-pontuacao')
        serializer = serializers.RankingSerializer(queryset, many=True)

        ranking = models.Estudante.objects.all().order_by(
            '-pontuacao').values_list('nome', 'pontuacao')
        return Response(list(ranking))


class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = models.Professor.objects.all().order_by('nome')
    serializer_class = serializers.ProfessorSerializer

    def list(self, request):
        queryset = models.Professor.objects.all().order_by('nome')
        serializer = serializers.ProfessorSerializer(queryset, many=True)
        professoras = models.Professor.objects.all().order_by('nome').values_list('nome')
        return Response(list(professoras))


class criaTituloViewSet(viewsets.ModelViewSet):
    queryset = models.Titulo.objects.all()
    serializer_class = serializers.criaTituloSerializer

    def create(self, request):
        serializer = serializers.criaTituloSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # salva os dados no banco
            serializer.save()
            # pega os dados que foram enviados pela requisição post
            data = request.data

            #  lista
            return Response(serializer.data)


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = models.Professor.objects.order_by('nome')
    serializer_class = serializers.ProfessorSerializer

    #queryset = models.Estudante.objects.order_by('nome')
    #serializer_class = serializers.EstudanteSerializer

    def list(self, request):
        queryset = models.Professor.objects.order_by('nome')
        serializer_class = serializers.ProfessorSerializer(queryset, many=True)
        professoras = models.Professor.objects.order_by(
            'nome').values_list('nome')
        alunas = models.Estudante.objects.order_by('nome').values_list('nome')

        usuarios = list(professoras) + list(alunas)
        usuarios.sort()

        return Response(usuarios)


class VisualizacaoViewSet(viewsets.ModelViewSet):
    queryset = models.Visualizacao.objects.all()
    serializer_class = serializers.VisualizacaoSerializer

    def create(self, request):
        serializer = serializers.VisualizacaoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # pega o ultimo usuario
            ultimo_usuario = list(
                models.Login.objects.all().order_by('id'))[-1].cpf
            serializer.validated_data['fkusuario'] = models.Estudante.objects.get(
                cpf=ultimo_usuario)
            serializer.validated_data['dataHora'] = django.utils.timezone.now()
            serializer.save()
            #####Estudante########
            # pega os dados que foram enviados pela requisição post
            data = serializer.validated_data
            # pega o id correspondente aestudante que fez o post para poder acessar a pontuação
            estudante_id = data["fkusuario"].id
            estudante_obj = models.Estudante.objects.get(id=estudante_id)
            # atualizando a pontuação
            estudante_obj.pontuacao += 5
            estudante_obj.save()

            data_atual = django.utils.timezone.now()
            tarefa_check = models.Tarefa.objects.filter(
                fkestudante=estudante_id, dataHora=data_atual, tipo='DC3')
            if tarefa_check.exists():
                tarefa_obj = models.Tarefa.objects.get(
                    fkestudante=estudante_id, dataHora=data_atual, tipo='DC3')
                if tarefa_obj.cumprida == 0:
                    tarefa_obj.cumprida = 1
                    tarefa_obj.save()
                    estudante_obj.pontuacao += 5  # estudante ganha 5 pontos por cumprir a tarefa
                    estudante_obj.save()

            # atualizando o título
            titulo_atual = models.listaTitulo.objects.get(
                fkestudante=estudante_id, tituloAtual=1)
            titulo_atual_obj = titulo_atual.fktitulo
            titulo_atual_nome = titulo_atual_obj.nome

            if estudante_obj.pontuacao > 840:
                if (estudante_obj.pontuacao <= 1680) and (titulo_atual_nome != 'Pontuação: 841 - 1680'):
                    titulo_atual.tituloAtual = 0
                    titulo_atual.save()
                    novo_titulo = models.Titulo.objects.get(
                        nome='Pontuação: 841 - 1680')
                    novo_titulo_obj = models.listaTitulo.objects.create(
                        fktitulo=novo_titulo, fkestudante=estudante_obj)
                    novo_titulo_obj.save()
                else:
                    if (estudante_obj.pontuacao > 1680) and (estudante_obj.pontuacao <= 3360) and (titulo_atual_nome != 'Pontuação: 1681 - 3360'):
                        titulo_atual.tituloAtual = 0
                        titulo_atual.save()
                        novo_titulo = models.Titulo.objects.get(
                            nome='Pontuação: 1681 - 3360')
                        novo_titulo_obj = models.listaTitulo.objects.create(
                            fktitulo=novo_titulo, fkestudante=estudante_obj)
                        novo_titulo_obj.save()
                    else:
                        if (estudante_obj.pontuacao > 3360) and (estudante_obj.pontuacao <= 6720) and (titulo_atual_nome != 'Pontuação: 3361 - 6720'):
                            titulo_atual.tituloAtual = 0
                            titulo_atual.save()
                            novo_titulo = models.Titulo.objects.get(
                                nome='Pontuação: 3361 - 6720')
                            novo_titulo_obj = models.listaTitulo.objects.create(
                                fktitulo=novo_titulo, fkestudante=estudante_obj)
                            novo_titulo_obj.save()
                        else:
                            if (estudante_obj.pontuacao > 6720) and (titulo_atual_nome != 'Pontuação: 6721 - oo'):
                                titulo_atual.tituloAtual = 0
                                titulo_atual.save()
                                novo_titulo = models.Titulo.objects.get(
                                    nome='Pontuação: 6721 - oo')
                                novo_titulo_obj = models.listaTitulo.objects.create(
                                    fktitulo=novo_titulo, fkestudante=estudante_obj)
                                novo_titulo_obj.save()

            return Response(serializer)

#############Páginas que dependem de dados do banco###################


def home(request):
    response_aluna = requests.get('http://127.0.0.1:8000/router/postagem/')
    response_prof = requests.get(
        'http://127.0.0.1:8000/router/postagem_armazenada/')
    response_user = requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]

    data_aluna = response_aluna.json()
    data_prof = response_prof.json()

    estudantes = [models.Estudante.objects.get(
        id=dict_est['fkusuario']).nome for dict_est in data_aluna]
    professora = [models.Professor.objects.get(
        id=dict_est['fkusuario']).nome for dict_est in data_prof]

    # identificar se é uma aluna que está logada
    eh_estudante = models.Estudante.objects.filter(cpf=user_ultimo["cpf"])
    c = {}
    if eh_estudante.exists():
        c['nao_aluna'] = False
    else:
        c['nao_aluna'] = True

    # preenchendo com alunas
    for i, aluna in enumerate(data_aluna):
        # print("\nAluna:{}\n".format(aluna))
        aluna['nome'] = estudantes[i]
        # print('\n Nome da aluna:{}\n'.format(aluna['nome']))
        aluna['estudante'] = True
        aluna['dataHora'] = datetime.datetime.strptime(
            aluna['dataHora'][:19], "%Y-%m-%dT%H:%M:%S")
        aluna['programada'] = False

    # preenchendo com professora
    for i, prof in enumerate(data_prof):
        # print("\nAluna:{}\n".format(professora))aluna['id_usuario'] = aluna['fkusuario']
        # print("\n i:{}\n".format(i))
        prof['nome'] = professora[i]
        # print('\n Nome da professora:{}\n'.format(prof['nome']))
        prof['estudante'] = False
        prof['dataHora'] = datetime.datetime.strptime(
            prof['dataHora'][:19], "%Y-%m-%dT%H:%M:%S")
        prof['programada'] = True

    lista_users = list(data_aluna + data_prof)
    lista_ordenado = sorted(
        lista_users, key=lambda x: x['dataHora'], reverse=True)
    # print("\n Primeiro post ver fkusuario:{}\n".format(lista_ordenado[0]))
    return render(request, 'home.html', {'data': lista_ordenado, 'c': c})


@csrf_protect
def login(request):
    c = {'erro_message': request.GET.get('erro', '')}
    if c['erro_message'] != "":
        c['is_erro'] = True
    else:
        c['is_erro'] = False
    return render(request, 'login.html', c)

# informações sobre título atual


def tituloAtual(request):
    response_user = requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]
    eh_estudante = models.Estudante.objects.filter(cpf=user_ultimo["cpf"])
    print("\n Aluna objeto:{}\n".format(eh_estudante))
    if eh_estudante.exists():
        list_titulos = models.listaTitulo.objects.filter(
            fkestudante=list(eh_estudante)[0]).order_by('-dataHora')
        print("\n Lista de Títulos de uma aluna:{}\n".format(list_titulos))
        # pega o titulo mais novo
        lista = list_titulos[0]
        obj_titulo_atual = lista.fktitulo
        pega_titulo = models.Titulo.objects.get(id=obj_titulo_atual.id).desc
        print("\n Aluna:{} \n Titulo atual:{}\n".format(
            list(eh_estudante)[0].nome, pega_titulo))

        # pegando as informações sobre pontos do próximo título
        prox_titulo_id = lista.fktitulo.id + 1
        titulo_prox = models.Titulo.objects.get(id=prox_titulo_id)
        qtdPontos_prox = titulo_prox.qtdPontos

        # nomes dos títulos que a aluna já teve
        nomes_titulos = [models.Titulo.objects.get(
            id=listTitulo.fktitulo_id).desc for listTitulo in list_titulos]
        c = {
            'aluna': {
                'nome': list(eh_estudante)[0].nome,
                'titulo': pega_titulo,
                'pontuacao': list(eh_estudante)[0].pontuacao,
                'pontos_para_prox_titulo': qtdPontos_prox - list(eh_estudante)[0].pontuacao,
            },
            'historico': [{'titulo': nomeTitulo, 'data': dateTime.dataHora} for nomeTitulo, dateTime in zip(nomes_titulos, list_titulos)

                          ]
        }
        c['nao_aluna'] = False
        return render(request, 'tituloAtual.html', {'c': c})
    else:
        c = {'nao_aluna': True}
        return render(request, 'home.html', {'c': c})

# Elencar todos os usuários


def listarTodosUsuarios(request):
    response_user = requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]
    eh_estudante = models.Estudante.objects.filter(cpf=user_ultimo["cpf"])
    print("\n Aluna objeto:{}\n".format(eh_estudante))
    if eh_estudante.exists():
        list_usuarios = models.Estudante.objects.order_by('nome')
        list_listaTitulo = []
        for usuario in list_usuarios:
            list_listaTitulo.append(models.listaTitulo.objects.filter(
                fkestudante=usuario).order_by('-dataHora')[0].fktitulo_id)
        print("\n Aluna:{} \n Pontuacao:{}\n".format(
            list(list_usuarios)[0].nome, list(list_usuarios)[0].pontuacao))
        listaAlunas = []

        for nomeAluna, id_titulo in zip(list_usuarios, list_listaTitulo):
            listaAlunas.append({'nome': nomeAluna.nome, 'pontos': nomeAluna.pontuacao,
                               'titulo': models.Titulo.objects.get(id=id_titulo).desc})

        c = {
            'usuarios': listaAlunas
        }
        c['nao_aluna'] = False
        return render(request, 'usuarios.html', {'c': c})

    else:
        c = {'nao_aluna': True}
        return render(request, 'home.html', {'c': c})

# Elencar todos os usuários com o mesmo titulo


def listarUsuariosMesmoTitulo(request):
    response_user = requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]
    eh_estudante = models.Estudante.objects.filter(cpf=user_ultimo["cpf"])
    print("\n Aluna objeto:{}\n".format(eh_estudante))
    if eh_estudante.exists():
        list_usuarios = models.Estudante.objects.all().order_by('nome')
        tituloSerMostrado_id = models.listaTitulo.objects.filter(
            fkestudante_id=list(eh_estudante)[0].id).order_by('-dataHora')[0].fktitulo_id
        nomeTituloSerMostrado = models.Titulo.objects.filter(
            id=tituloSerMostrado_id)[0].desc
        list_UsuariosMesmoTitulo = []
        for usuario in list_usuarios:
            if tituloSerMostrado_id == list(models.listaTitulo.objects.filter(fkestudante=usuario).order_by('-dataHora'))[0].fktitulo_id:
                list_UsuariosMesmoTitulo.append(models.listaTitulo.objects.filter(
                    fkestudante=usuario).order_by('-dataHora')[0].fkestudante)
        print("\n Aluna:{} \n Pontuacao:{}\n".format(
            list(list_usuarios)[0].nome, list(list_usuarios)[0].pontuacao))
        listaAlunas = []

        for nomeAluna in list_UsuariosMesmoTitulo:
            listaAlunas.append(
                {'nome': nomeAluna.nome, 'pontos': nomeAluna.pontuacao})

        c = {
            'usuarios': listaAlunas
        }
        c['nao_aluna'] = False
        return render(request, 'usuariosMesmoTitulo.html', {'c': c})
    else:
        c = {'nao_aluna': True}
        return render(request, 'home.html', {'c': c})

# Ranking


def ranking(request):
    response_user = requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]
    eh_estudante = models.Estudante.objects.filter(cpf=user_ultimo["cpf"])
    print("\n Aluna objeto:{}\n".format(eh_estudante))
    if eh_estudante.exists():
        list_usuarios = models.Estudante.objects.all().order_by('-pontuacao')
        listaAlunas = []

        for nomeAluna in list_usuarios:
            listaAlunas.append(
                {'nome': nomeAluna.nome, 'pontos': nomeAluna.pontuacao})

        c = {
            'usuarios': listaAlunas
        }
        c['nao_aluna'] = False
        return render(request, 'ranking.html', {'c': c})

    else:
        c = {'nao_aluna': True}
        return render(request, 'home.html', {'c': c})


def tarefas(request):
    response_user = requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]
    eh_estudante = models.Estudante.objects.filter(cpf=user_ultimo["cpf"])
    print("\n Aluna objeto:{}\n".format(eh_estudante))
    if eh_estudante.exists():

        tarefaAtual = models.Tarefa.objects.filter(
            cumprida=False,fkestudante=list(eh_estudante)[0]).order_by('-dataHora')
        
        # Lista de tarefas já concluida
        list_tarefasConcluidas = models.Tarefa.objects.filter(
            cumprida=True, fkestudante=list(eh_estudante)[0]).order_by('-dataHora')

        tarefasConcluidas = []
        for item in list_tarefasConcluidas:
            tarefasConcluidas.append(
                {'tipo': item.desc, 'pontos': item.qtdPontos, 'data': item.dataHora})

        print(tarefaAtual)

        if len(tarefaAtual) > 0:
            tarefaAtual = tarefaAtual[0]
            atual = {
                'tipo': tarefaAtual[0].desc,
                'pontos': tarefaAtual[0].qtdPontos,
                'cumprida': tarefaAtual[0].cumprida,
            }
        else:
            atual = {
                'tipo': "",
                'pontos': "",
                'cumprida': True,
            }

        c = {
            'atual': atual,
            'historico': tarefasConcluidas
        }
        c['nao_aluna'] = False
        return render(request, 'tarefas.html', {'c': c})
    else:
        c = {'nao_aluna': True}
        return render(request, 'tarefas.html', {'c': c})


@csrf_protect
def criarPost(request):
    response_user = requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]
    # estudantes = [models.Estudante.objects.get(id=dict_est['fkusuario']).nome for dict_est in data_aluna ]
    eh_estudante = models.Estudante.objects.filter(cpf=user_ultimo["cpf"])
    eh_professor = models.Professor.objects.filter(cpf=user_ultimo["cpf"])
    if eh_estudante.exists():
        print(list(eh_estudante)[0].id)
        c = {'id_user': list(eh_estudante)[0].id}
        c['nao_aluna'] = False
        return render(request, 'criarPost.html', {'c': c})
    elif eh_professor.exists():
        c = {'id_user': list(eh_professor)[0].id}
        c['nao_aluna'] = True
        return render(request, 'criarPost_professora.html', {'c': c})


@csrf_protect
def comentario(request):
    response_user = requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]
    eh_estudante = models.Estudante.objects.filter(cpf=user_ultimo["cpf"])
    c = {}
    if eh_estudante.exists():
        c['nao_aluna'] = False
    else:
        c['nao_aluna'] = True

    return render(request, 'comentario.html', {'c': c})


def visualizacao(request, id_usuario, estudante, id_postagem, programada, data_postagem):
    response_user = requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]
    eh_estudante = models.Estudante.objects.filter(cpf=user_ultimo["cpf"])
    c = {}
    if eh_estudante.exists():
        c['nao_aluna'] = False

    else:
        c['nao_aluna'] = True

    if programada == 'True':
        postagem = list(models.PostagemArmazenada.objects.filter(
            fkusuario_id=id_usuario, id=id_postagem))[0]
        c['titulo'] = postagem.titulo
        c['texto'] = postagem.texto
        c['nome'] = models.Professor.objects.get(id=postagem.fkusuario_id).nome
        c['dataHora'] = data_postagem
    else:
        postagem = list(models.Postagem.objects.filter(
            fkusuario_id=id_usuario, id=id_postagem))[0]
        c['titulo'] = postagem.titulo
        c['texto'] = postagem.texto
        c['nome'] = models.Estudante.objects.get(id=postagem.fkusuario_id).nome
        c['dataHora'] = data_postagem

    c['id_user'] = id_usuario
    c['id_postagem'] = id_postagem
    c['estudante'] = estudante
    c['programada'] = programada
    c['dataHora'] = data_postagem

    # criando uma instância de visualização
    # isso é só pra aluna, pois só ela recebe os pontos
    if eh_estudante.exists():
        if programada == 'True':
            # objeto existe de visualização
            objeto_visu_postagem = models.Visualizacao.objects.filter(
                fkpostagem_id=id_postagem)
            if objeto_visu_postagem.exists() == False:
                # preciso registrar o aluno que visualizou, pra ele ganhar ponto
                visu = models.Visualizacao.objects.create(foiVisualizado=True,
                                                          fkestudante_id=list(
                                                              eh_estudante)[0].id,
                                                          fkprogramada_id=id_postagem)
                visu.save()
                visualizacao_ponto(eh_estudante)
        else:
            # objeto existe de visualização
            objeto_visu_programada = models.Visualizacao.objects.filter(
                fkprogramada_id=id_postagem)
            if objeto_visu_programada.exists() == False:
                # preciso registrar o aluno que visualizou, pra ele ganhar ponto
                visu = models.Visualizacao.objects.create(foiVisualizado=True,
                                                          fkestudante_id=list(
                                                              eh_estudante)[0].id,
                                                          fkpostagem_id=id_postagem)
                visu.save()
                visualizacao_ponto(eh_estudante)
    return render(request, 'visualizacao.html', {'c': c})


@csrf_protect
def comentario(request, id_usuario, estudante, id_postagem, programada, data_postagem):
    ###quem está logado###
    response_user = requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]
    eh_estudante = models.Estudante.objects.filter(cpf=user_ultimo["cpf"])
    c = {}
    if eh_estudante.exists():
        c['nao_aluna'] = False

    else:
        c['nao_aluna'] = True
    ###
    ###pegando as informações da postagem, para saber em qual postagem está sendo feita a postagem###
    if programada == 'True':
        postagem = list(models.PostagemArmazenada.objects.filter(
            fkusuario_id=id_usuario, id=id_postagem))[0]
        c['titulo'] = postagem.titulo
        c['texto'] = postagem.texto
        c['nome'] = models.Professor.objects.get(id=postagem.fkusuario_id).nome
        c['dataHora'] = data_postagem
    else:
        postagem = list(models.Postagem.objects.filter(
            fkusuario_id=id_usuario, id=id_postagem))[0]
        c['titulo'] = postagem.titulo
        c['texto'] = postagem.texto
        c['nome'] = models.Estudante.objects.get(id=postagem.fkusuario_id).nome
        c['dataHora'] = data_postagem

    c['id_user'] = id_usuario
    c['id_postagem'] = id_postagem
    # se é um aluno
    c['estudante'] = estudante
    # se a postagem é do tipo programada
    c['programada'] = programada
    # data que a postagem foi feita
    c['dataHora'] = data_postagem

    ###pegando os comentarios que já foram feitas###
    response_comentario = requests.get('http://127.0.0.1:8000/router/comentario/')
    comentarios_banco = response_comentario.json()
    lista_comentarios = []
    # texto = models.CharField(max_length=10000)
    # fkestudante = models.ForeignKey(Estudante,on_delete=models.CASCADE, blank=True, null=True)
    # fkprofessor = models.ForeignKey(Professor,on_delete=models.CASCADE, blank=True, null=True)
    # dataHora = models.DateTimeField(auto_now_add = True)

    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=None)
    # object_id = models.PositiveIntegerField(default=None)
    # fkpostagem = GenericForeignKey('content_type', 'object_id')
    for comentario in comentarios_banco:
        if type(comentario['fkestudante'])!=type(None):
            comentario['nome'] = models.Estudante.objects.get(id=comentario['fkestudante_id'])
        else:
            comentario['nome'] = models.Professor.objects.get(id=comentario['fkprofessor_id'])
        # comentario['object_id'] = 

            


    return render(request,'comentario.html',{'c':c,'lista_comentarios':comentarios_banco})



# @csrf_protect 
# def criarTarefa(request):
#     response_user= requests.get('http://127.0.0.1:8000/router/login/')
#     # respose_tarefa = request.get('http://127.0.0.1:8000/router/tarefa/')

#     data_user = response_user.json()
#     user_ultimo = data_user[-1]
#     eh_estudante =  models.Estudante.objects.filter(cpf = user_ultimo["cpf"])
#     print("\n Ultimo estudante objeto:{}\n".format(eh_estudante))
#     c={}
#     print("\n É Estudante:{}\n".format(eh_estudante.exists()))
#     if eh_estudante.exists():
#         c['nao_aluna'] = False
#         c['id_user'] = models.Estudante.objects.get(user_ultimo['id']).id
#     else:
#         c['nao_aluna'] = True
#         print("\n Professora:{}\n".format(models.Professor.objects.get(user_ultimo['id'])))
#         c['id_user'] = models.Professor.objects.get(user_ultimo['id']).id

#     return render(request,'criarTarefa.html',{'c':c})


################Páginas estáticas################
# página estática de títulos
def titulos(request):
    response_user = requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]
    eh_estudante = models.Estudante.objects.filter(cpf=user_ultimo["cpf"])
    c = {}
    if eh_estudante.exists():
        c['nao_aluna'] = False
    else:
        c['nao_aluna'] = True
    return render(request, 'titulos.html', {'c': c})


def tutorial(request):
    response_user = requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]
    eh_estudante = models.Estudante.objects.filter(cpf=user_ultimo["cpf"])
    c = {}
    if eh_estudante.exists():
        c['nao_aluna'] = False
    else:
        c['nao_aluna'] = True
    return render(request, 'tutorial.html', {'c': c})


def sobre(request):
    response_user = requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]
    eh_estudante = models.Estudante.objects.filter(cpf=user_ultimo["cpf"])
    c = {}
    if eh_estudante.exists():
        c['nao_aluna'] = False
    else:
        c['nao_aluna'] = True
    return render(request, 'sobre.html', {'c': c})


def politicas(request):
    response_user = requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]
    eh_estudante = models.Estudante.objects.filter(cpf=user_ultimo["cpf"])
    c = {}
    if eh_estudante.exists():
        c['nao_aluna'] = False
    else:
        c['nao_aluna'] = True
    return render(request, 'politicas.html', {'c': c})


def assistencia(request):
    response_user = requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]
    eh_estudante = models.Estudante.objects.filter(cpf=user_ultimo["cpf"])
    c = {}
    if eh_estudante.exists():
        c['nao_aluna'] = False
    else:
        c['nao_aluna'] = True
    return render(request, 'assistenciaEstudantil.html', {'c': c})


def professoras(request):
    response_user = requests.get('http://127.0.0.1:8000/router/login/')
    data_user = response_user.json()
    user_ultimo = data_user[-1]
    eh_estudante = models.Estudante.objects.filter(cpf=user_ultimo["cpf"])
    c = {}
    if eh_estudante.exists():
        c['nao_aluna'] = False
    else:
        c['nao_aluna'] = True
    return render(request, 'professoras.html', {'c': c})



#######################Funções auxiliares###########################
def visualizacao_ponto(eh_estudante):
    #####Estudante########
    estudante_id = list(eh_estudante)[0].id
    # pega o id correspondente aestudante que fez o post para poder acessar a pontuação
    estudante_obj = models.Estudante.objects.get(id=estudante_id)
    # atualizando a pontuação
    estudante_obj.pontuacao += 5
    estudante_obj.save()

    data_atual = django.utils.timezone.now()
    tarefa_check = models.Tarefa.objects.filter(
        fkestudante=estudante_id, dataHora=data_atual, tipo='DC1')
    if tarefa_check.exists():
        tarefa_obj = models.Tarefa.objects.get(
            fkestudante=estudante_id, dataHora=data_atual, tipo='DC1')
        if tarefa_obj.cumprida == 0:
            tarefa_obj.cumprida = 1
            tarefa_obj.save()
            estudante_obj.pontuacao += 5  # estudante ganha 5 pontos por cumprir a tarefa
            estudante_obj.save()

    # atualizando o título
    titulo_atual = models.listaTitulo.objects.get(
        fkestudante=estudante_id, tituloAtual=1)
    titulo_atual_obj = titulo_atual.fktitulo
    titulo_atual_nome = titulo_atual_obj.nome

    if estudante_obj.pontuacao > 840:
        if (estudante_obj.pontuacao <= 1680) and (titulo_atual_nome != 'Pontuação: 841 - 1680'):
            titulo_atual.tituloAtual = 0
            titulo_atual.save()
            novo_titulo = models.Titulo.objects.get(
                nome='Pontuação: 841 - 1680')
            novo_titulo_obj = models.listaTitulo.objects.create(
                fktitulo=novo_titulo, fkestudante=estudante_obj)
            novo_titulo_obj.save()
        else:
            if (estudante_obj.pontuacao > 1680) and (estudante_obj.pontuacao <= 3360) and (titulo_atual_nome != 'Pontuação: 1681 - 3360'):
                titulo_atual.tituloAtual = 0
                titulo_atual.save()
                novo_titulo = models.Titulo.objects.get(
                    nome='Pontuação: 1681 - 3360')
                novo_titulo_obj = models.listaTitulo.objects.create(
                    fktitulo=novo_titulo, fkestudante=estudante_obj)
                novo_titulo_obj.save()
            else:
                if (estudante_obj.pontuacao > 3360) and (estudante_obj.pontuacao <= 6720) and (titulo_atual_nome != 'Pontuação: 3361 - 6720'):
                    titulo_atual.tituloAtual = 0
                    titulo_atual.save()
                    novo_titulo = models.Titulo.objects.get(
                        nome='Pontuação: 3361 - 6720')
                    novo_titulo_obj = models.listaTitulo.objects.create(
                        fktitulo=novo_titulo, fkestudante=estudante_obj)
                    novo_titulo_obj.save()
                else:
                    if (estudante_obj.pontuacao > 6720) and (titulo_atual_nome != 'Pontuação: 6721 - oo'):
                        titulo_atual.tituloAtual = 0
                        titulo_atual.save()
                        novo_titulo = models.Titulo.objects.get(
                            nome='Pontuação: 6721 - oo')
                        novo_titulo_obj = models.listaTitulo.objects.create(
                            fktitulo=novo_titulo, fkestudante=estudante_obj)
                        novo_titulo_obj.save()
