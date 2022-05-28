from django.contrib import admin
from .models import Usuario
from .models import Estudante
from .models import Professor
from .models import Postagem
from .models import PostagemProgramada

# Register your models here.
admin.site.register(Estudante)
admin.site.register(Professor)
admin.site.register(Postagem)
admin.site.register(PostagemProgramada)
