from django.shortcuts import render
from rest_framework import viewsets
from .serializer import TreinoModelSerializer
from .models import TreinoModel
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication,SessionAuthentication

class TreinoModelViewset(viewsets.ModelViewSet):
    queryset = TreinoModel.objects.all()
    serializer_class = TreinoModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication,SessionAuthentication]
    http_method_names = ['get','post','patch','delete']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(usuario=self.request.user)
        buscar = self.request.query_params.get('q','')
        if buscar != '':
            qs = qs.filter(treino_nome__icontains=buscar)
        return  qs
