from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
import datetime
import django
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

"""
Título:
- Pontuação: 0 - 840: Bonnie Prado Pinto;
- Pontuação: 841 - 1680: Angelica Ross;
- Pontuação: 1681 - 3360: Shirley Ann Jackson;
- Pontuação: 3361 - 6720: Timnit Gebru;
- Pontuação: 7560 - oo: Marie Van Brittan Brown.
"""

class Titulo(models.Model):
    titulos = (
        ("Pontuação: 0 - 840","Bonnie Prado Pinto"),
        ("Pontuação: 841 - 1680","Angelica Ross"),
        ("Pontuação: 1681 - 3360", "Shirley Ann Jackson"),
        ("Pontuação: 3361 - 6720","Timnit Gebru"),
        ("Pontuação: 7560 - oo","Marie Van Brittan Brown"),
    )
    nome = models.CharField(choices=titulos, max_length=100, default="Pontuação: 0 - 840")
    qtdPontos = models.IntegerField() # quantos pontos são necessários para se ter esse título
    estudante = models.ManyToManyField(Estudante, through='listaTitulo')

class listaTitulo(models.Model): # títulos que as estudantes já tiveram, assim como o título atual
    fktitulo = models.ForeignKey(Titulo,on_delete=models.CASCADE)
    fkestudante = models.ForeignKey(Estudante,on_delete=models.CASCADE)
    dataHora = models.DateTimeField(auto_now_add = True)
    tituloAtual = models.BooleanField(default=1)

"""
Tarefa:
- Tabela referente às tarefas associadas às alunas;
"""
class Tarefa(models.Model):
    desc_choice = (
        ("DC1", "Ler uma postagem."),
        ("DC2", "Publicar um comentário."),
        ("DC3", "Publicar uma postagem."),
    )
    tipo = models.CharField(choices=desc_choice, max_length=30, default="DC1")
    #dataHora = models.DateTimeField(auto_now_add = True)
    dataHora = models.DateField(auto_now_add = True, db_column='data')
    cumprida = models.BooleanField(default=0)
    fkestudante = models.ForeignKey(Estudante,on_delete=models.CASCADE, default=None)
    qtdPontos = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.tipo == 'DC1':
            self.qtdPontos = 5
        else:
            if self.tipo == 'DC2':
                self.qtdPontos = 10
            else:
                self.qtdPontos = 15    
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('tipo', 'dataHora')

class Notificacao(models.Model):
    descricao = models.CharField(max_length=100)
    dataHora = models.DateTimeField(auto_now_add = True)

"""
Comentario:
- Tabela referente aos comentários feitos por alunas;
- Valor de pontos ganhos: 10;
"""
class Comentario(models.Model):
    texto = models.CharField(max_length=10000)
    fkestudante = models.ForeignKey(Estudante,on_delete=models.CASCADE)     
    dataHora = models.DateTimeField(auto_now_add = True)
    qtdPontos = models.IntegerField(default=10)
    #fkpostagem = models.ForeignKey(Postagem,on_delete=models.CASCADE, blank=True, null=True)
    #fkprogramada = models.ForeignKey(PostagemArmazenada,on_delete=models.CASCADE, blank=True, null=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=None)
    object_id = models.PositiveIntegerField(default=None)
    fkpostagem = GenericForeignKey('content_type', 'object_id')


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
    comentarios = GenericRelation(Comentario)

"""
Postagem Armazenada:
- Tem esse nome pois quando não são programadas para um dia específico, o sistema armazena e posta depois;
- Tabela referente as postagens feitas por professoras;
"""
class PostagemArmazenada(models.Model):
    titulo = models.CharField(max_length=10000)
    texto = models.CharField(max_length=10000)
    dataHora = models.DateTimeField(default=django.utils.timezone.now, null=True)
    fkusuario = models.ForeignKey(Professor,on_delete=models.CASCADE)
   
    comentarios = GenericRelation(Comentario)    

class Visualizacao(models.Model):
    foiVisualizado = models.BooleanField(default=False)
    ehPontoExtra = models.BooleanField(default=False)
    qtdPontos = models.IntegerField()
    fkpostagem = models.ForeignKey(Postagem,on_delete=models.CASCADE, blank=True, null=True)
    fkprogramada = models.ForeignKey(PostagemArmazenada,on_delete=models.CASCADE, blank=True, null=True)  
    