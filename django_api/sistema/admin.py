from django.contrib import admin
from .models import Usuario
from .models import Estudante
from .models import Professor
from .models import Postagem
from .models import PostagemArmazenada
from .models import Titulo
from .models import listaTitulo
from .models import Tarefa
from .models import Notificacao
from .models import Comentario

# Register your models here.
admin.site.register(Estudante)
admin.site.register(Professor)
admin.site.register(Postagem)
admin.site.register(PostagemArmazenada)
admin.site.register(Titulo)
admin.site.register(listaTitulo)
admin.site.register(Tarefa)
admin.site.register(Notificacao)
admin.site.register(Comentario)
