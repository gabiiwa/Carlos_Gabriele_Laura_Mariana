from django.db import models

# Create your models here.
class Usuario(models.Model):
    senha=models.CharField(max_length=20)
    cpf = models.IntegerField()
    nome = models.CharField(max_length=100)
    def __str__(self):
        return self.nome

class Professor(Usuario):
    siape = models.IntegerField()

class Estudante(Usuario):
    matricula = models.CharField(11)

