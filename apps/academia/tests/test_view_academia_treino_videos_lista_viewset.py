from rest_framework.test import APITestCase
from rest_framework.status import (HTTP_405_METHOD_NOT_ALLOWED,HTTP_400_BAD_REQUEST,
                                   HTTP_201_CREATED,HTTP_200_OK,HTTP_204_NO_CONTENT,
                                   HTTP_404_NOT_FOUND)
from apps.academia.tests.utils_geradores_base import GeradoresBaseMixin
from django.urls import reverse


class TreinoVideosListaViewSetTest(GeradoresBaseMixin,APITestCase):
    def setUp(self):
      self.username, self.usuario = self.criar_usuario_logout_logar()
      self.url = reverse('treino-videos-listas-list')

    def test_treino_videos_lista_viewset_get_retorna_codigo_200(self):
        resposta = self.client.get(self.url)
        self.assertEqual(resposta.status_code,HTTP_200_OK)

    def test_treino_videos_lista_viewset_post_retorna_codigo_405(self):
        reposta = self.client.post(self.url,data={})
        self.assertEqual(reposta.status_code,HTTP_405_METHOD_NOT_ALLOWED)

    def test_treino_videos_lista_viewset_put_retorna_codigo_405(self):
        resposta = self.client.put(f'{self.url}1/')
        self.assertEqual(resposta.status_code,HTTP_405_METHOD_NOT_ALLOWED)


    def test_treino_videos_lista_viewset_patch_retorna_codigo_405(self):
        resposta = self.client.patch(f'{self.url}1/')
        self.assertEqual(resposta.status_code , HTTP_405_METHOD_NOT_ALLOWED)

    def test_treino_videos_lista_viewset_delete_retorna_405(self):
        resposta = self.client.delete(self.url+'1/')
        self.assertEqual(resposta.status_code,HTTP_405_METHOD_NOT_ALLOWED)

    def test_treino_videos_lista_viewset_get_retorna_query_somente_do_usuario(self):
        # Criar TreinosVideos
        treino_2 = self.criar_treino(treino='treino2',usuario=self.usuario)
        self.criar_treino_videos(usuario=self.usuario)
        self.criar_treino_videos(usuario=self.usuario,treino=treino_2)

        #Criar treino cliente 2
        cliente_2_username = 'Cliente_2'
        cliente_2_password = 'UserPass2' 

        cliente_2 = self.cadastro_usuario(username=cliente_2_username,password=cliente_2_password)
        self.criar_treino_videos(usuario=cliente_2)

        # Reposta Cliente 1
        resposta = self.client.get(self.url)
        self.assertEqual(len(resposta.data),2)
        self.assertEqual(resposta.data[0]['usuario'],self.username)
        self.assertEqual(resposta.data[1]['usuario'],self.username)

        # Reposta cliente 2
        self.criar_usuario_logout_logar(username=cliente_2_username,password=cliente_2_password)

        resposta = self.client.get(self.url)
        self.assertEqual(len(resposta.data),1)
        self.assertEqual(resposta.data[0]['usuario'],cliente_2.username)

    def test_treino_videos_lista_viewset_get_retona_campos_necessarios(self):
        self.criar_treino_videos(usuario=self.usuario)
        resposta = self.client.get(self.url)

        # Campos necessarios
        campos = set(resposta.data[0])
        campos_necessarios = {'ordem', 'videos', 'treino_id', 'treino', 
                              'usuario', 'id'}

        self.assertEqual(campos,campos_necessarios)
        self.assertEqual(len(campos),len(campos_necessarios))
        
        # Campos Videos Necessarios
        campos_videos = set(resposta.data[0]['videos'][0])
        campos_videos_necessarios = {'id_video', 'video_nome', 'video_url', 
                                     'informacao', 'video_id_didatico', 
                                     'equipamento', 'imagem', 'video_id_youtube', 
                                     'grupo_muscular'}
        self.assertEqual(len(campos_videos),len(campos_videos_necessarios))
        self.assertEqual(campos_videos,campos_videos_necessarios)

    def test_treino_videos_lista_viewset_get_pk_retorna_somente_do_usuario(self):
        # Cliente 1
        self.criar_treino_videos(usuario=self.usuario,treino='Treino_1')
        self.criar_treino_videos(usuario=self.usuario,treino='Treino_2')
        self.criar_treino_videos(usuario=self.usuario,treino='Treino_3')

        # Cliente 2
        cliente_2_username = 'Cliente_2'
        cliente_2_password = 'ClientPass'
        cliente_2 = self.cadastro_usuario(username='Cliente_2',password='ClientPass')
        self.criar_treino_videos(usuario=cliente_2,treino='Treino_cliente_2')

        # Reposta cliente 1
        # item nao do usuario
        resposta = self.client.get(self.url+'4/')
        self.assertEqual(resposta.status_code,HTTP_404_NOT_FOUND)

        # item do usuario
        resposta = self.client.get(self.url+'3/')
        self.assertEqual(resposta.status_code,HTTP_200_OK)
        self.assertEqual(resposta.data['usuario'],self.username)

        # Resposta Cliente 2
        self.criar_usuario_logout_logar(username=cliente_2_username,password=cliente_2_password)
        # item nao do usuario
        resposta = self.client.get(self.url+'3/')
        self.assertEqual(resposta.status_code,HTTP_404_NOT_FOUND)

        # item do usuario
        resposta = self.client.get(self.url+'4/')
        self.assertEqual(resposta.status_code,HTTP_200_OK)
        self.assertEqual(resposta.data['usuario'],cliente_2_username)
