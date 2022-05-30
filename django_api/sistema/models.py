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

class Postagem(models.Model):
    texto = models.CharField(max_length=10000)
    fkusuario = models.ForeignKey(Estudante,on_delete=models.CASCADE)
    
class PostagemProgramada(Postagem):
    post_date = models.DateField()
    