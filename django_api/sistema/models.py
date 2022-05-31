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
    pontuacao = models.IntegerField()
    titulo = models.CharField(max_length=100)

class Postagem(models.Model):
    texto = models.CharField(max_length=10000)
    fkusuario = models.ForeignKey(Estudante,on_delete=models.CASCADE)
    
class PostagemProgramada(models.Model):
    texto = models.CharField(max_length=10000)
    post_date = models.DateField()
    fkusuario = models.ForeignKey(Professor,on_delete=models.CASCADE)
    tag_choice = (
        ("TG1", "Normal"),
        ("TG2", "Extra"),
    )
    tag = models.CharField(choices=tag_choice, max_length=10, default="TG1") #marcador que pode ser de dois tipos: tarefa diária ou tarefa extra
