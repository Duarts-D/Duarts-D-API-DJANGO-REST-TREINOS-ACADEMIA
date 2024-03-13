from django.shortcuts import render
from rest_framework import viewsets
from apps.academia import serializers
from .models import TreinoModel,TreinoVideosmodel,VideoModel,TreinosCompartilhadosModel
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED,HTTP_404_NOT_FOUND,HTTP_400_BAD_REQUEST
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView,RetrieveAPIView,GenericAPIView
from apps.academia.utils import criar_slug
from django.db.utils import IntegrityError
from django.db import transaction

QTD_TREINO_REPETIDO = 5

class TreinoCRUDViewset(viewsets.ModelViewSet):
    queryset = TreinoModel.objects.all()
    serializer_class = serializers.TreinoModelSerializer
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
    serializer_class = serializers.TreinoVideosSerializer
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
    serializer_class = serializers.TreinoVideosSerializerPost
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
        reposta_serializer = serializers.TreinoVideosSerializer(save)
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
        reposta_serializer = serializers.TreinoVideosSerializer(self.get_object())
        return Response(reposta_serializer.data)

    def perform_update(self, serializer):
        serializer.save(slug_compartilhado='')

class TreinoCompartilhadoCreate(CreateAPIView):
    serializer_class = serializers.TreinoCompartilhadoSerializerCreate
    permission_classes = [IsAuthenticated]
    authentication_classes =[BasicAuthentication,SessionAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        treino_url_compartilhada = serializer.validated_data['treino'].slug_compartilhado
        headers = self.get_success_headers(serializer)
        # Retorna se ja tiver slug criada
        if treino_url_compartilhada:
            return Response({'url':treino_url_compartilhada}, status=HTTP_201_CREATED, headers=headers)
        else:
            treino_url_compartilhada = self.perform_create(serializer)

        return Response({'url':treino_url_compartilhada},status=HTTP_201_CREATED, headers=headers)

    def perform_create(self,serializer):
        # salvando o model compartilhado
        treino = serializer.validated_data['treino']
        treino_str = str(treino)
        ordem = treino.ordem
        slug = criar_slug(treino_str)
        videos = treino.videos.all()
        
        treino_compartilhado , criar = TreinosCompartilhadosModel.objects.get_or_create(treino=treino_str,
                                                                       ordem=ordem,
                                                                       )
        if criar:
            treino_compartilhado.videos.set(videos)
            treino_compartilhado.slug = slug
            treino_compartilhado.save()

        # salvando o slug na instancia copiada
        treino.slug_compartilhado = slug
        treino.save()
        
        return slug

class TreinoCompartilhadoRetrieve(RetrieveAPIView):
    queryset = TreinosCompartilhadosModel.objects.prefetch_related('videos','videos__equipamento','videos__grupo_muscular')
    serializer_class = serializers.TreinoCompartilhadoSerializerRetrieve
    permission_classes = []
    authentication_classes =[]
    lookup_field = 'slug'

class TreinoCompartilhadoAdd(CreateAPIView):
    serializer_class = serializers.TreinoCompartilhadoSerializerAdd
    permission_classes = [IsAuthenticated]
    authentication_classes =[BasicAuthentication,SessionAuthentication]

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response('Sucesso',status=HTTP_201_CREATED)

    def perform_create(self, serializer):
        usuario = self.request.user
        treino_compartilhado = serializer.validated_data['slug_compartilhado']
        i = 0
        while True:
            try:
                with transaction.atomic():
                    treino = TreinoModel.objects.create(
                        usuario=usuario,
                        treino_nome=('_'*i) + treino_compartilhado.treino + ('_'*i)
                        )
            except IntegrityError:
                i += 1 
                if i == QTD_TREINO_REPETIDO :
                    raise IntegrityError('Limite atigido, favor apague treinos com'
                                         f' nome que contem {treino_compartilhado.treino}.')
            else:
                break
        criar_treino_videos = TreinoVideosmodel.objects.create(
            usuario = usuario,
            treino = treino,
            ordem = treino_compartilhado.ordem,
            slug_compartilhado = treino_compartilhado.slug
        )
        criar_treino_videos.videos.set(treino_compartilhado.videos.all())
        criar_treino_videos.save()