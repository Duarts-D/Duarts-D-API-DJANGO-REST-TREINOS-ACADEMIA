from django.shortcuts import render
from rest_framework import viewsets
from .serializer import TreinoModelSerializer,TreinoVideosSerializer,TreinoVideosSerializerPost
from .models import TreinoModel,TreinoVideosmodel,VideoModel
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED,HTTP_404_NOT_FOUND,HTTP_400_BAD_REQUEST

class TreinoCRUDViewset(viewsets.ModelViewSet):
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

class TreinoVideoslistaViewSet(viewsets.ModelViewSet):
    queryset = TreinoVideosmodel.objects.prefetch_related('videos','videos__equipamento','videos__grupo_muscular')
    serializer_class = TreinoVideosSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes =[BasicAuthentication,SessionAuthentication]
    http_method_names = ['get',]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(usuario=self.request.user)
        qs = qs.select_related('treino','usuario')
        return qs
        
class TreinoVideosCUDViewSet(viewsets.ModelViewSet):
    queryset = TreinoVideosmodel.objects.all()
    serializer_class = TreinoVideosSerializerPost
    permission_classes = [IsAuthenticated]
    authentication_classes =[BasicAuthentication,SessionAuthentication]
    http_method_names = ['post','patch','delete']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(usuario=self.request.user)
        return qs
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            status = HTTP_404_NOT_FOUND if serializer.errors.get('treino') else HTTP_400_BAD_REQUEST
            return Response(serializer.errors,status=status)
        
        save = self.perform_create(serializer)
        reposta_serializer = TreinoVideosSerializer(save)
        headers = self.get_success_headers(reposta_serializer.data)
        return Response(reposta_serializer.data, status=HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        usuario = self.request.user
        item = serializer.data
        videos = item.get('videos')
        ordem = item.get('ordem')
        treino = TreinoModel.objects.filter(id=item['treino'],usuario=usuario).first()
       
        treino_video , criado = TreinoVideosmodel.objects.get_or_create(
            usuario=usuario,treino=treino,ordem=ordem)
        if videos is not None:
            treino_video.videos.set(videos)
            treino_video.save()
        
        return treino_video
    

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        
        reposta_serializer = TreinoVideosSerializer(self.get_object())
        return Response(reposta_serializer.data)
