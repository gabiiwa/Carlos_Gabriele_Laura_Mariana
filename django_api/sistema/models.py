from django.db import models

# Create your models here.
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    senha=models.CharField(max_length=20)
    cpf = models.IntegerField()
    nome = models.CharField(max_length=100)
    def __str__(self):
        return self.nome

class Professor(Usuario):
    siape = models.IntegerField()

class Estudante(Usuario):
    matricula = models.CharField(11)

class Postagem(models.Model):
    texto = models.CharField(max_length=10000)
    fkusuario = models.ForeignKey(id_usuario, on_delete=models.CASCADE)
    def __str__(self):
        return self.fkusuario.name
class PostagemProgramada(Postagem):
    post_date = models.DateField()
    