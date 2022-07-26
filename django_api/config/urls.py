"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from sistema import views


#declarando rotas para criar as urls das páginas que serão criadas
router = routers.DefaultRouter()
router.register(r'postagem', views.PostagemViewSet)
router.register(r'postagem_armazenada', views.PostagemArmazenadaViewSet)
router.register(r'tarefa', views.TarefaViewSet)
router.register(r'comentario', views.ComentarioViewSet)
router.register(r'login', views.LoginViewSet)
router.register(r'ranking', views.RankingViewSet)
router.register(r'lista_professoras', views.ProfessorViewSet)
router.register(r'titulo', views.criaTituloViewSet)
router.register(r'lista_usuarios', views.UsuarioViewSet, basename ='lista_usuarios')

router_tarefa = routers.DefaultRouter()
router_tarefa.register(r'criaTarefa',views.TarefaViewSet)
urlpatterns = [
    path('', views.login, name='login'),
    path('router/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('titulos/', views.titulos, name="titulos"),
    path('tutorial/', views.tutorial, name="tutorial"),
    path('sobre/', views.sobre, name="sobre"),
    path('usuarios/', views.listarTodosUsuarios, name="usuarios"),
    path('usuariosMesmoTitulo/', views.listarUsuariosMesmoTitulo, name="usuariosMesmoTitulo"),
    path('politicas/', views.politicas, name="politicas"),
    path('titulo-atual/', views.tituloAtual, name="tituloAtual"),
    path('assistencia/', views.assistencia, name="assistencia"),
    path('professoras/', views.professoras, name="professoras"),
    path('criarPost/', views.criarPost, name="criarPostagem"),
    path('ranking/', views.ranking, name="ranking"),
    path('visualizar/int:id_usuario/int:id_postagem', views.visualizacao, name='vizualizar'),
    path('comentario/int:id_usuario/boolean:estudante/int:id_postagem', views.comentario, name="comentario"),
    path('tarefas/', views.tarefas, name="tarefas"),
    # path('teste',include(router_tarefa)),
    # path('visualizar/int:id', views.visualizar, name='vizualizar'),
    
    
]
