#### Passos para rodar a aplicação 
##### Backend

``` shell
$ source venv/bin/activate #ativar venv, precisa estar na pasta django_api

```
## Instalando dependecias - django
```shell
$ pip install django
$ pip install djangorestframework
```

## Rodando a aplicação django
```shell
$ python manage.py runserver
```
## Acessar o banco pelo django
precisa ter criado um super user:
```shell
$ python manage.py createsuperuser
```