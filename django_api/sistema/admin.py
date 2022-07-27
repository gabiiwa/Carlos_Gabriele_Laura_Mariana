from django.contrib import admin
from .models import Usuario
from .models import Estudante
from .models import Professor
from .models import Postagem
from .models import PostagemArmazenada
from .models import Titulo
from .models import listaTitulo
from .models import Tarefa
from .models import Comentario
from .models import Login
from .models import Visualizacao
class EstudanteAdmin(admin.ModelAdmin):
    list_display = ('cpf','nome','matricula','pontuacao')
    list_display_links = ('cpf','nome','matricula')


# Register your models here.
admin.site.register(Estudante,EstudanteAdmin)
admin.site.register(Professor)
admin.site.register(Postagem)
admin.site.register(PostagemArmazenada)
admin.site.register(Titulo)
admin.site.register(listaTitulo)
admin.site.register(Tarefa)
admin.site.register(Comentario)
admin.site.register(Login)
admin.site.register(Visualizacao)
