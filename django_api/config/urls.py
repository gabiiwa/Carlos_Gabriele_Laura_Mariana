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
router.register(r'lista_titulos', views.TituloViewSet)

urlpatterns = [
    path('', views.login, name='login'),
    path('router/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('titulos/', views.titulos, name="titulos"),
    # path('visualizar/', views.visualizar, name='vizualizar'),
    # path('home/', views.home, name='home'),
    
]
