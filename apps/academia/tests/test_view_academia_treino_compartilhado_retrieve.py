from rest_framework.test import APITestCase
from rest_framework.status import (HTTP_405_METHOD_NOT_ALLOWED,HTTP_200_OK,HTTP_404_NOT_FOUND)
from django.urls import resolve
from apps.academia.models import TreinosCompartilhadosModel
from apps.academia import views
from apps.academia.serializers import TreinoCompartilhadoSerializerRetrieve
from apps.academia.tests.test_utils_gerados_base import GeradoresBaseMixin
from parameterized import parameterized


class TreinoCompartilhadoRetrieveTest(GeradoresBaseMixin,APITestCase):
    def setUp(self) -> None:
        self.url = 'compartilhar-retrieve'

    def test_treinocompartilhado_retrieve_view_url_correta(self):
        resultado = resolve(self.url_retrieve_slug(url=self.url))
        self.assertIs(resultado.func.view_class,views.TreinoCompartilhadoRetrieve)

    def test_treinocompartilhado_retrieve_view_utiliza_query_treino_compartilhado(self):
        esperado = TreinosCompartilhadosModel
        view  = views.TreinoCompartilhadoRetrieve()
        resposta = view.queryset.model
        self.assertEqual(resposta, esperado)

    def test_treinocompartilhado_retrieve_view_utiliza_serializer_treinocompartilhadoRetrieve(self):
        esperado = TreinoCompartilhadoSerializerRetrieve
        
        view = views.TreinoCompartilhadoRetrieve()
        resposta = view.serializer_class
        self.assertEqual(resposta,esperado)

    def test_treinocompartilhado_retrieve_view_utilize_slug_para_localizado_query_objeto(self):
        esperado = 'slug'

        view = views.TreinoCompartilhadoRetrieve()
        self.assertEqual(view.lookup_field,esperado)

    def test_treinocompartilhado_retrieve_view_permission_classe_nao_necessario(self):
        esperado = []
        view = views.TreinoCompartilhadoRetrieve()
        resultado = view.permission_classes
        self.assertEqual(resultado,esperado)
    
    def test_treinocompartilhado_retrieve_view_authentication_classe_nao_necessario(self):
        esperado = []
        view = views.TreinoCompartilhadoRetrieve()
        resultado = view.authentication_classes
        self.assertEqual(resultado,esperado)
        

    def test_treinocompartilhado_retrieve_get_retorna_status_200(self):
        treino_c = self.criar_treino_compartilhado()
        url = self.url_retrieve_slug(url=self.url,slug=treino_c.slug)
        
        resposta = self.client.get(url)
        self.assertEqual(resposta.status_code,HTTP_200_OK) 

    def test_treinocompartilhado_retrieve_get_retorna_status_404(self):
        url = self.url_retrieve_slug(url=self.url)
        resposta = self.client.get(url)
        self.assertEqual(resposta.status_code, HTTP_404_NOT_FOUND)

    def test_treinocompartilhado_retrieve_post_retorna_status_405(self):
        url = self.url_retrieve_slug(url=self.url,)
    
        resposta = self.client.post(url)
        self.assertEqual(resposta.status_code, HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_treinocompartilhado_retrieve_put_retorna_status_405(self):
        url = self.url_retrieve_slug(url=self.url,)
    
        resposta = self.client.put(url)
        self.assertEqual(resposta.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_treinocompartilhado_retrieve_patch_retorna_status_405(self):
        url = self.url_retrieve_slug(url=self.url,)
    
        resposta = self.client.patch(url)
        self.assertEqual(resposta.status_code, HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_treinocompartilhado_retrieve_delete_retorna_status_405(self):
        url = self.url_retrieve_slug(url=self.url,)
        resposta = self.client.delete(url)
        self.assertEqual(resposta.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    @parameterized.expand([
        ('id'), ('videos'),('ordem'), ('slug')]
    )
    def test_treinocompartilhado_retrieve_retorna_campos_id_treino_videos_ordem_slug(self,campo):
        treino = self.criar_treino_compartilhado()
        url = self.url_retrieve_slug(url=self.url,slug=treino.slug)
        
        resposta = self.client.get(url)
        resposta_data = resposta.data
        # Verificando se os campos estao na resposta
        self.assertIn(campo,resposta_data)

    def test_treinocompartilhadp_retrieve_retorna_campos_com_valor_correto(self):
        videos = self.criar_videos_multiplicos(qtd=2)
        treino = self.criar_treino_compartilhado()
        treino.videos.set(videos)
        treino.save()

        esperados_videos = treino.videos.all()

        url = self.url_retrieve_slug(url=self.url,slug=treino.slug)
        resposta = self.client.get(url)
        resposta_data = resposta.data

        self.assertEqual(resposta_data['id'],treino.id)
        self.assertEqual(resposta_data['ordem'],treino.ordem)        
        self.assertEqual(resposta_data['slug'],treino.slug)        
        
        videos_data = resposta_data['videos']
        for i , video in enumerate(videos_data):
            esperado_video = esperados_videos[i]
            data_esperado_video = [
                esperado_video.id,
                esperado_video.video_nome,
                esperado_video.video_id_youtube,
                esperado_video.video_url,
                esperado_video.informacao,
                None if not esperado_video.imagem else esperado_video.imagem ,
                esperado_video.video_id_didatico,
                esperado_video.grupo_muscular.__str__(),
                esperado_video.equipamento.__str__(),
                ]
            resposta_data_lista = list(video.values())
            self.assertEqual(resposta_data_lista,data_esperado_video)
    
    def test_treinocompartilhado_retrieve_videos_retorna_9_campos(self):
        videos = self.criar_videos_multiplicos(qtd=1)
        treino = self.criar_treino_compartilhado()
        treino.videos.set(videos)
        treino.save()

        esperado_quantidade_campos = 9

        url = self.url_retrieve_slug(url=self.url,slug=treino.slug)
        resposta = self.client.get(url)
        resposta_data = resposta.data['videos'][0]
        
        self.assertEqual(len(resposta_data),esperado_quantidade_campos)