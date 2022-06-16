from django.db import models
# Create your models here.
class Usuario(models.Model):
    cpf = models.IntegerField()
    nome = models.CharField(max_length=100)

    class Meta:
       abstract = True
       ordering = ['nome'] 


    def __str__(self):
        return self.nome

class Professor(Usuario):
    siape = models.IntegerField()

class Estudante(Usuario):
    matricula = models.CharField(max_length=11)
    pontuacao = models.IntegerField(default = 0)

class Titulo(models.Model):
    nome = models.CharField(max_length=100)
    qtdPontos = models.IntegerField() # quantos pontos são necessários para se ter esse título
    estudante = models.ManyToManyField(Estudante, through='listaTitulo')

class listaTitulo(models.Model): # títulos que as estudantes já tiveram, assim como o título atual
    fktitulo = models.ForeignKey(Titulo,on_delete=models.CASCADE)
    fkestudante = models.ForeignKey(Estudante,on_delete=models.CASCADE)
    dataHora = models.DateTimeField(auto_now_add = True)
    tituloAtual = models.BooleanField()

class Tarefa(models.Model):
    descricao = models.CharField(max_length=100)
    dataHora = models.DateTimeField()
    cumprida = models.BooleanField()

class Notificacao(models.Model):
    descricao = models.CharField(max_length=100)
    dataHora = models.DateTimeField(auto_now_add = True)

"""
Postagem:
- Tabela referente as postagens feitas por alunas;
- Valor de pontos ganhos: 15;
"""
class Postagem(models.Model):
    titulo = models.CharField(max_length=10000)
    texto = models.CharField(max_length=10000)
    fkusuario = models.ForeignKey(Estudante,on_delete=models.CASCADE)
    dataHora = models.DateTimeField(auto_now_add = True, null=True)
    qtdPontos = models.IntegerField(default=15)

"""
Postagem Armazenada:
- Tem esse nome pois quando não são programadas para um dia específico, o sistema armazena e posta depois;
- Tabela referente as postagens feitas por professoras;
"""
class PostagemArmazenada(models.Model):
    titulo = models.CharField(max_length=10000)
    texto = models.CharField(max_length=10000)
    post_date = models.DateTimeField(null=True, blank=True)
    fkusuario = models.ForeignKey(Professor,on_delete=models.CASCADE)
    tag_choice = (
        ("TG1", "Normal"),
        ("TG2", "Extra"),
    )
    tag = models.CharField(choices=tag_choice, max_length=10, default="TG1") #marcador que pode ser de dois tipos: tarefa diária ou tarefa extra
    programada = models.BooleanField()

class Comentario(models.Model):
    texto = models.CharField(max_length=10000)
    fkpostagem = models.ForeignKey(Postagem,on_delete=models.CASCADE, blank=True, null=True)
    fkprogramada = models.ForeignKey(PostagemArmazenada,on_delete=models.CASCADE, blank=True, null=True)  
    fkEstudante = models.ForeignKey(Estudante,on_delete=models.CASCADE)     
    dataHora = models.DateTimeField(auto_now_add = True)
    qtdPontos = models.IntegerField()
    

class Visualizacao(models.Model):
    foiVisualizado = models.BooleanField(default=False)
    ehPontoExtra = models.BooleanField(default=False)
    qtdPontos = models.IntegerField()
    fkpostagem = models.ForeignKey(Postagem,on_delete=models.CASCADE, blank=True, null=True)
    fkprogramada = models.ForeignKey(PostagemArmazenada,on_delete=models.CASCADE, blank=True, null=True)  
    