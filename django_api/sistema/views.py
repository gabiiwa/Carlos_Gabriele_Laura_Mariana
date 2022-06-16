from django.shortcuts import render

from rest_framework import viewsets
from sistema import serializers
from sistema import models
from rest_framework.response import Response
# import requests

class PostagemViewSet(viewsets.ModelViewSet):
    queryset = models.Postagem.objects.all().order_by('dataHora')
    serializer_class = serializers.PostagemSerializer
    def create(self, request):
        serializer = serializers.PostagemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
             data = request.data
             estudante_id = data.get("fkusuario")
             estudante_obj = models.Estudante.objects.get(id=estudante_id)
             print("Pontos que quero inserir:{}".format(15))
             print("\n Pontos que tenho {}".format(estudante_obj.pontuacao))
             estudante_obj.pontuacao += 15
             estudante_obj.save()
             return Response(serializer.data)
class PostagemArmazenadaViewSet(viewsets.ModelViewSet):
    queryset = models.PostagemArmazenada.objects.all().order_by('post_date')
    serializer_class = serializers.PostagemArmazenadaSerializer