from rest_framework.test import APITestCase
from apps.academia import serializers
from apps.academia.tests._utils_geradores_base import GeradoresBaseMixin
from apps.academia  import models
from rest_framework.relations import StringRelatedField,PrimaryKeyRelatedField,SlugRelatedField
from pytest import mark


class TreinoModelSeriliazerTest(APITestCase):
    def test_treinoModelserializer_model_utilizado_e_treinomodel(self):
        esperado_model = models.TreinoModel
        serializer = serializers.TreinoModelSerializer()
        serializer_model = serializer.Meta.model
        self.assertEqual(serializer_model,esperado_model)

    def test_treinoModelserializer_campo_usuario_somente_para_leitura(self):
        dados = {'treino_nome':''}
        serializer = serializers.TreinoModelSerializer(data=dados)
        campo_leitura = serializer.fields['usuario'].read_only

        self.assertTrue(campo_leitura)

class VideosSerializersTest(APITestCase):
    def test_videos_serializer_model_utilizado_e_videosmodel(self):
        esperado_model  = models.VideoModel
        serializer = serializers.VideosSerializer()
        serializer_model = serializer.Meta.model
        self.assertEqual(serializer_model,esperado_model)
        
    def test_videos_serializer_campos_necessarios(self):
        serializer = serializers.VideosSerializer()
        campos_necessarios= {'video_id_didatico', 'informacao', 'video_nome', 
                             'video_url', 'imagem', 'grupo_muscular','equipamento', 
                             'video_id_youtube', 'id_video'}
        campos = set(serializer.fields.keys())

        self.assertEqual(len(campos),9)
        self.assertEqual(campos,campos_necessarios)
    
class TreinoVideosSerializerTest(GeradoresBaseMixin,APITestCase):
    
    def test_treino_videos_serializer_model_utilizado_e_treinovideosModel(self):
        esperado_model = models.TreinoVideosmodel
        serializer = serializers.TreinoVideosSerializer()
        serializer_model = serializer.Meta.model
        self.assertEqual(serializer_model,esperado_model)

    def test_treino_videos_serializer_campo_necessario(self):
        serializer = serializers.TreinoVideosSerializer()
        campos_necessario = {'usuario', 'treino', 'treino_id', 'ordem', 'videos', 'id'}        
        campos = set(serializer.fields.keys())

        self.assertEqual(len(campos),6)
        self.assertEqual(campos,campos_necessario)

    def test_treino_videos_serializer_campo_video_esta_utilizando_serializer_de_videos_serializer(self):
        video1 = self.criar_video()
        treino = self.criar_treino()
        usuario = self.cadastro_usuario(username='Usario_do_video')
        treino_videos = models.TreinoVideosmodel.objects.create(
            usuario = usuario,
            treino=treino
        )
        treino_videos.videos.add(video1)
        treino_videos.save()
        

        serializer = serializers.TreinoVideosSerializer(treino_videos)

        data_video = serializer.data['videos'][0]
        data_video = set(data_video.keys())
        campos_videos_serializer = {'imagem', 'video_id_youtube', 
                                  'grupo_muscular', 'id_video', 'video_id_didatico', 
                                  'equipamento', 'video_nome', 'video_url', 'informacao'}
        self.assertEqual(data_video,campos_videos_serializer)
    
    def test_treino_videos_serializer_campos_usuario_e_treino_modo_stringrelatedfield_e_read_only(self):
        serializer = serializers.TreinoVideosSerializer()
        campo_usuario = serializer.fields['usuario']
        campo_treino = serializer.fields['treino']
        self.assertIsInstance(campo_usuario,StringRelatedField)
        self.assertIsInstance(campo_treino,StringRelatedField)
        self.assertTrue(campo_usuario.read_only)
        self.assertTrue(campo_treino.read_only)


    def test_treino_videos_serializer_campos_treino_id_modo_stringrelatefield_e_read_only(self):
        serializer = serializers.TreinoVideosSerializer()
        campo_treino_id = serializer.fields['treino_id']
        self.assertIsInstance(campo_treino_id,PrimaryKeyRelatedField)
        self.assertTrue(campo_treino_id.read_only)

class TreinoVideosSerializerPostTest(GeradoresBaseMixin,APITestCase):
    def test_treino_videos_serializerPost_model_utilizado_e_treinovideosModel(self):
        esperado_model = models.TreinoVideosmodel
        serializer = serializers.TreinoVideosSerializerPost()
        serializer_model = serializer.Meta.model
        self.assertEqual(serializer_model,esperado_model)

    def test_treino_videos_serializerPost_campos_necessario(self):
        serializer = serializers.TreinoVideosSerializerPost()
        campos = set(serializer.fields.keys())
        campos_necessario = {'ordem', 'id', 'treino', 'videos'}
        self.assertEqual(campos,campos_necessario)

class TreinoCompartilhadoSerializerCreate(GeradoresBaseMixin,APITestCase):
    def test_treinocompartilhado_serializer_retrieve_model_utilizado_treinocompartilhadosmodel(self):
        esperado_model = models.TreinosCompartilhadosModel
        serializer = serializers.TreinoCompartilhadoSerializerRetrieve()
        serializer_model = serializer.Meta.model
        self.assertEqual(serializer_model,esperado_model)

    def test_treinocompartilhado_serializer_retrieve_campos_necessario(self):        
        serializer = serializers.TreinoCompartilhadoSerializerRetrieve()
        campos = set(serializer.fields.keys())
        campos_necessario = {'id', 'treino', 'videos', 'ordem','slug'}
        self.assertEqual(campos,campos_necessario)

class TestTreinoCompartilhadoSerialzierAdd():
    def test_treinocompartilhado_add_serializer_campo_slug_compartilhado_e_slugfield(self):
        serializer = serializers.TreinoCompartilhadoSerializerAdd()
        esperado = SlugRelatedField
        resultado = serializer.fields['slug_compartilhado']
        assert isinstance(resultado,esperado)
    
    @mark.django_db
    def test_treinocompartilhado_add_serializer_parametro_do_slug_compartilhado_slug_field_e_o_campo_do_model_slug_de_treino_compartilhado(self,treino_compartilhado,serializer_add_compartilhado):
        campo = serializer_add_compartilhado.fields['slug_compartilhado']
        resultado_slug = campo.slug_field
        # O campo da query set para utilizar como filtro do slugfield
        assert resultado_slug == 'slug'
        # O queryset utilizado para o slugfield
        resultado_queryset = campo.queryset
        assert isinstance(resultado_queryset[0], models.TreinosCompartilhadosModel) 

    def test_treinocompartilhado_add_serializer_campos(self,serializer_add_compartilhado):
        resultado = set(serializer_add_compartilhado.fields.keys())
        assert len(resultado) == 1
        assert 'slug_compartilhado' in resultado
    