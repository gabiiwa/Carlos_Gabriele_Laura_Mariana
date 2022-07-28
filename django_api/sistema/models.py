from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime
import django
# Create your models here.

"""
Usuario:
- Tabela de usuários do sistema.
"""
class Usuario(models.Model):
    cpf = models.IntegerField()
    nome = models.CharField(max_length=100)

    class Meta:
       abstract = True
       ordering = ['nome'] 


    # def __str__(self):
    #     return self.nome

"""
Professor:
- Tabela de professoras.
"""
class Professor(Usuario):
    siape = models.IntegerField()

"""
Estudante:
- Tabela de alunas.
"""
class Estudante(Usuario):
    matricula = models.CharField(max_length=11)
    pontuacao = models.IntegerField(default = 0)

"""
Título:
- Pontuação: 0 - 840: Bonnie Prado Pinto;
- Pontuação: 841 - 1680: Angelica Ross;
- Pontuação: 1681 - 3360: Shirley Ann Jackson;
- Pontuação: 3361 - 6720: Timnit Gebru;
- Pontuação: 6721 - oo: Marie Van Brittan Brown.
"""

class Titulo(models.Model):
    titulos = (
        ("Pontuação: 0 - 840","Bonnie Prado Pinto"),
        ("Pontuação: 841 - 1680","Angelica Ross"),
        ("Pontuação: 1681 - 3360", "Shirley Ann Jackson"),
        ("Pontuação: 3361 - 6720","Timnit Gebru"),
        ("Pontuação: 6721 - oo","Marie Van Brittan Brown"),
    )
    nome = models.CharField(choices=titulos, max_length=100, default="Pontuação: 0 - 840")
    desc = models.CharField(max_length = 30, default = "Bonnie Prado Pinto")
    qtdPontos = models.IntegerField() # quantos pontos são necessários para se ter esse título
    estudante = models.ManyToManyField(Estudante, through='listaTitulo')

    def save(self, *args, **kwargs):
        if self.nome == 'Pontuação: 0 - 840':
            self.qtdPontos = 0
            self.desc = 'Bonnie Prado Pinto'
        else:
            if self.nome == 'Pontuação: 841 - 1680':
                self.qtdPontos = 841
                self.desc = 'Angelica Ross'
            else:
                if self.nome == 'Pontuação: 1681 - 3360':
                    self.qtdPontos = 1681
                    self.desc = 'Shirley Ann Jackson'
                else:
                    if self.nome == 'Pontuação: 3361 - 6720':
                        self.qtdPontos = 3361
                        self.desc = 'Timnit Gebru'
                    else:
                        self.qtdPontos = 6721
                        self.desc = 'Marie Van Brittan Brown'
        super().save(*args, **kwargs)

"""
Lista Titulo:
- Tabela que relaciona títulos da tabela Titulo com estudantes.
"""
class listaTitulo(models.Model): # títulos que as estudantes já tiveram, assim como o título atual
    fktitulo = models.ForeignKey(Titulo,on_delete=models.CASCADE)
    fkestudante = models.ForeignKey(Estudante,on_delete=models.CASCADE)
    dataHora = models.DateTimeField(auto_now_add = True)
    tituloAtual = models.BooleanField(default=1)

    class Meta:
        unique_together = ('fkestudante', 'fktitulo')

    @receiver(post_save, sender = Estudante)
    def associa_Titulo(sender, instance, created, **kwargs):
        if created:
            titulo = Titulo.objects.get(nome = 'Pontuação: 0 - 840')
            listaTitulo.objects.create(fktitulo = titulo, fkestudante = instance)

"""
Tarefa:
- Tabela referente às tarefas diárias associadas às alunas;
- Tarefas podem ser de três tipos: leitura de postagem, publicação de comentário
  e publicação de postagem;
- Cada tipo de tarefa possui uma pontuação associada.  
"""
class Tarefa(models.Model):
    desc_choice = (
        ("DC1", "Ler uma postagem."),
        ("DC2", "Publicar um comentário."),
        ("DC3", "Publicar uma postagem."),
    )
    tipo = models.CharField(choices=desc_choice, max_length=30, default="DC1")
    desc = models.CharField(max_length = 30, default = "Ler uma postagem.")
    #dataHora = models.DateTimeField(auto_now_add = True)
    dataHora = models.DateField(auto_now_add = True, db_column='data')
    cumprida = models.BooleanField(default=0)
    fkestudante = models.ForeignKey(Estudante,on_delete=models.CASCADE, default=None)
    qtdPontos = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.tipo == 'DC1':
            self.qtdPontos = 5
            self.desc = 'Ler uma postagem.'
        else:
            if self.tipo == 'DC2':
                self.qtdPontos = 10
                self.desc = 'Publicar um comentário.'
            else:
                self.qtdPontos = 15
                self.desc = 'Publicar uma postagem.'    
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('tipo', 'dataHora','fkestudante')


"""
Comentario:
- Tabela referente aos comentários feitos por usuários;
- Valor de pontos ganhos pela aluna: 10.
"""
class Comentario(models.Model):
    texto = models.CharField(max_length=10000)
    fkestudante = models.ForeignKey(Estudante,on_delete=models.CASCADE, blank=True, null=True)
    fkprofessor = models.ForeignKey(Professor,on_delete=models.CASCADE, blank=True, null=True)   
    dataHora = models.DateTimeField(auto_now_add = True)
    qtdPontos = models.IntegerField(default=10)
    #fkpostagem = models.ForeignKey(Postagem,on_delete=models.CASCADE, blank=True, null=True)
    #fkprogramada = models.ForeignKey(PostagemArmazenada,on_delete=models.CASCADE, blank=True, null=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=None)
    object_id = models.PositiveIntegerField(default=None)
    fkpostagem = GenericForeignKey('content_type', 'object_id')


"""
Postagem:
- Tabela referente às postagens feitas por alunas;
- Valor de pontos ganhos: 15.
"""
class Postagem(models.Model):
    titulo = models.CharField(max_length=10000)
    texto = models.CharField(max_length=10000)
    fkusuario = models.ForeignKey(Estudante,on_delete=models.CASCADE)
    dataHora = models.DateTimeField(null=True, default=django.utils.timezone.now)
    qtdPontos = models.IntegerField(default=15)
    comentarios = GenericRelation(Comentario)

"""
Postagem Armazenada:
- Tem esse nome pois quando não são programadas para um dia específico, o sistema armazena e posta depois;
- Tabela referente às postagens feitas por professoras.
"""
class PostagemArmazenada(models.Model):
    titulo = models.CharField(max_length=10000)
    texto = models.CharField(max_length=10000)
    dataHora = models.DateTimeField(default=django.utils.timezone.now, null=True)
    fkusuario = models.ForeignKey(Professor,on_delete=models.CASCADE)
   
    comentarios = GenericRelation(Comentario)    

"""
Visualização:
- Permite que as alunas vejam a postagem inteira e ganhem pontos por elas;
- Valor de pontos ganhos: 5.
"""
class Visualizacao(models.Model):
    foiVisualizado = models.BooleanField(default=False)
    fkestudante = models.ForeignKey(Estudante,on_delete=models.CASCADE, blank=True, null=True)
    fkpostagem = models.ForeignKey(Postagem,on_delete=models.CASCADE, blank=True, null=True)
    fkprogramada = models.ForeignKey(PostagemArmazenada,on_delete=models.CASCADE, blank=True, null=True)

    # class Meta:
    #     unique_together = ('fkestudante','fkpostagem','fkprogramada')  

"""
Login:
- Tabela relacionada ao login de usuários no sistema.
"""
class Login(models.Model):
    senha = models.IntegerField()
    cpf =  models.IntegerField()
    eh_usuario = models.BooleanField(default=False)
    dataHora = models.DateTimeField(default=django.utils.timezone.now, null=True)
    