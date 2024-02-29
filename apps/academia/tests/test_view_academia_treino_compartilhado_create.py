from rest_framework.test import APITestCase
from rest_framework.status import (HTTP_405_METHOD_NOT_ALLOWED,HTTP_201_CREATED)
from apps.academia.tests.utils_geradores_base import GeradoresBaseMixin
from django.urls import reverse
from apps.academia.models import TreinoVideosmodel,TreinosCompartilhadosModel

class TreinoCompartilhadoCreateViewTest(GeradoresBaseMixin,APITestCase):
    def setUp(self) -> None:
        self.username , self.usuario = self.criar_usuario_logout_logar()
        self.url = reverse('compartilhar-criar')

    def fixture_treino_video(self,usuario):
        """
        -> Criar um treino_video vinculado ao usuario e dict de 'treino' com id.
        """
        treino_video = self.criar_treino_videos(usuario=usuario)
        dados = {'treino': treino_video.id}
        return treino_video , dados
    
    def test_treinocompartilhadocreate_get_retorna_status_405(self):
        resultado = self.client.get(self.url)
        # Resposta
        self.assertEqual(resultado.status_code,HTTP_405_METHOD_NOT_ALLOWED)

    def test_treinocompartilhadocreate_post_retorna_status_201(self):
        treino_video = self.criar_treino_videos(usuario=self.usuario)
        dados = {'treino':treino_video.id}
        resultado = self.client.post(self.url,data=dados)
        # Resposta
        self.assertEqual(resultado.status_code,HTTP_201_CREATED)


    def test_treinocompratilhadocreate_put_retorna_status_405(self):
        resultado = self.client.put(self.url)
        # Resposta
        self.assertEqual(resultado.status_code,HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_treinocompratilhadocreate_patch_retorna_status_405(self):
        resultado = self.client.patch(self.url)
        # Resposta
        self.assertEqual(resultado.status_code,HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_treinocompratilhadocreate_delete_retorna_status_405(self):
        resultado = self.client.delete(self.url)
        # Resposta
        self.assertEqual(resultado.status_code,HTTP_405_METHOD_NOT_ALLOWED)
    

    def test_treino_compartilhadocreate_retornar_campo_url(self):
        _ , dados = self.fixture_treino_video(usuario=self.usuario)

        resultado = self.client.post(self.url,data=dados)
        resultad_data = resultado.data
        campo_esperado = 'url'

        # Resposta
        self.assertIn(campo_esperado, resultado.data)        
        self.assertEqual(len(resultad_data),1 )

    def test_treino_compartilhadocreate_slug_compartilhado_retorna_a_slug(self):
        slug =  'test1234rxsa109i32ksca-98u1'

        treino_video , dados = self.fixture_treino_video(usuario=self.usuario)
        treino_video.slug_compartilhado = slug
        treino_video.save()
        
        resultado = self.client.post(self.url,data=dados)
        resultado_data = resultado.data['url']

        # resposta
        self.assertEqual(resultado_data, slug)

    def test_treino_compartilhadocreate_criar_compartilhamentomodel_utilizando_campos_do_treinovideomodel(self):
        treino_video , dados = self.fixture_treino_video(usuario=self.usuario)
        video_2 = self.criar_video()
        video_3 = self.criar_video()
        treino_video.videos.add(video_2)
        treino_video.videos.add(video_3)
        treino_video.save()

        resposta_url = self.client.post(self.url,data=dados).data['url']

        treino_compartilhado = TreinosCompartilhadosModel.objects.get(slug=resposta_url)
        
        # Videos
        videos_treino = treino_video.videos.all()
        compartilhar_video = treino_compartilhado.videos.all()
        # Reposta 
        # Verificar se os campos estao salvo iguamente 
        campo_treino = str(treino_video.treino) == treino_compartilhado.treino
        campo_videos = all(video1 == video2 for video1 , video2 in zip(videos_treino,compartilhar_video))
        campo_ordem = treino_video.ordem == treino_compartilhado.ordem
        campo_slug = TreinoVideosmodel.objects.filter(slug_compartilhado=treino_compartilhado.slug).exists()
        self.assertTrue(campo_treino)
        self.assertTrue(campo_videos)
        self.assertTrue(campo_ordem)
        self.assertTrue(campo_slug)

    def test_treino_compartilhadocreate_criar_uma_novo_slug_e_salva_no_treino_video_model(self):
        treino_video , dados = self.fixture_treino_video(usuario=self.usuario)

        resultado = self.client.post(self.url,data=dados)
        resultado_url = resultado.data['url']
        # Resposta
        self.assertEqual(resultado.status_code, HTTP_201_CREATED)
        # Verificar slug esta sendo salvado no model que foi utilizado para criacao do compartilhamento
        treino_video_slug = TreinoVideosmodel.objects.get(id=treino_video.id).slug_compartilhado
        self.assertEqual(resultado_url,treino_video_slug)

    