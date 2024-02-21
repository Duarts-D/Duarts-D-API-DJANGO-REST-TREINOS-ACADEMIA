from rest_framework.test import APITestCase
from rest_framework.status import (HTTP_405_METHOD_NOT_ALLOWED,HTTP_400_BAD_REQUEST,
                                   HTTP_201_CREATED,HTTP_200_OK,HTTP_204_NO_CONTENT,
                                   HTTP_404_NOT_FOUND)
from apps.academia.tests.utils_geradores_base import GeradoresBaseMixin
from django.urls import reverse
from collections import OrderedDict

class FixtureTreinoVideos(GeradoresBaseMixin):
    def criarTreinosVideos(self,usuario):
        """Cria um treino e um treino-video vinculado ao usuario"""
        treino = self.criar_treino(usuario=usuario)
        treino_video = self.criar_treino_videos(usuario=usuario,treino=treino)
        return treino , treino_video

class TreinoVideosCUDViewsetTest(FixtureTreinoVideos,GeradoresBaseMixin,APITestCase):
    """ Testes da viewset TreinoVideosCUDViewSet"""
    def setUp(self):
        self.username, self.usuario = self.criar_usuario_logout_logar()
        self.url = reverse('treino-videos-list')

    def test_treino_videos_cud_viewset_get_bloqueado_retorna_codigo_405(self):
        # Testando metodo get esta bloqueado
        resposta = self.client.get(self.url)
        self.assertEqual(resposta.status_code,HTTP_405_METHOD_NOT_ALLOWED)

    def test_treino_video_cud_viewset_get_pk_bloqueado_retorna_codigo_405(self):
        # Testando metodo get pk esta bloqueado
        resposta = self.client.get(self.url+'2/')
        self.assertEqual(resposta.status_code,HTTP_405_METHOD_NOT_ALLOWED)

    def test_treino_videos_cud_viewset_post_permitido_retorna_codigo_201(self):
        # Testando metodo post esta permitido
        treino = self.criar_treino(usuario=self.usuario)
        reposta = self.client.post(self.url,data={'treino':treino.id})
        self.assertEqual(reposta.status_code,HTTP_201_CREATED)

    def test_treino_videos_cud_viewset_put_bloqueado_retorna_codigo_405(self):
        # Testando metodo put esta bloqueado
        resposta = self.client.put(f'{self.url}1/')
        self.assertEqual(resposta.status_code,HTTP_405_METHOD_NOT_ALLOWED)

    def test_treino_videos_cud_viewset_patch_permitido_retorna_codigo_200(self):
        # Testando metodo patch permitido
        _,treino_video = self.criarTreinosVideos(usuario=self.usuario)
        video = self.criar_video(publicado=True) 
        resposta = self.client.patch(f'{self.url}{treino_video.id}/',data={'videos':video.id})
        self.assertEqual(resposta.status_code , HTTP_200_OK)

    def test_treino_videos_cud_viewset_delete_permitido_retorna_204(self):
        # Testando metodo delete permitido 
        _ ,treino_video =  self.criarTreinosVideos(self.usuario)
        resposta = self.client.delete(f'{self.url}{treino_video.id}/')
        self.assertEqual(resposta.status_code,HTTP_204_NO_CONTENT)

    def test_treino_videos_cud_viewset_campos_necessario_treino(self):
        # Testando o campos obrigatorio do metodo post
        resposta = self.client.post(self.url,data={})
        campo = resposta.data['treino'][0]
        error_msg = str(campo)
        error_esperado = 'Este campo é obrigatório.'
        error_status = campo.code

        self.assertEqual(error_msg,error_esperado)
        self.assertEqual(error_status,'required')
        self.assertEqual(len(resposta.data),1)

    def test_treino_videos_cud_viewset_metodo_post_201_create_passando_treino_videos_e_ordem_retorna_id_usuario_treino_treino_id_videos_ordem(self):
        # Criando um treino vinculado ao usuario authenticado
        treino = self.criar_treino(usuario=self.usuario)
        # Criando um video
        video = self.criar_video(publicado=True)
        ordem = '1' 
        # Reposta de criacao do metodo post
        resposta = self.client.post(self.url,data={'treino':treino.id,
                                                   'videos':video.id,
                                                   'ordem':ordem
                                                   })
        resposta_status = resposta.status_code
        resposta_data = resposta.data
        # Campos de retorno permitidos
        esperado_data = {'id': 1, 'usuario': 'Cliente', 
                         'treino': 'Treino', 'treino_id': 1, 
                         'videos': [OrderedDict([('id_video', 1), 
                         ('video_nome', 'Video Teste'), 
                         ('video_id_youtube', 'iey118'), 
                         ('video_url', 'https://www.youtube.com/embed/iey118'), 
                         ('informacao', None), ('imagem', None), 
                         ('video_id_didatico', None), 
                         ('grupo_muscular', 'Muscular'), 
                         ('equipamento', 'Equipamento')])], 'ordem':'1'}
        
        self.assertEqual(resposta_status,HTTP_201_CREATED)
        self.assertEqual(len(resposta_data),6)
        self.assertEqual(resposta_data,esperado_data)
        #Campos videos permitidos
        esperando_video =  [OrderedDict([('id_video', 1),
                      ('video_nome', 'Video Teste'),
                      ('video_id_youtube', 'iey118'),
                      ('video_url', 'https://www.youtube.com/embed/iey118'),
                      ('informacao', None),
                      ('imagem', None),
                      ('video_id_didatico', None),
                      ('grupo_muscular', 'Muscular'),
                      ('equipamento', 'Equipamento')])]
        # Testando retorno dos campos correspondente
        self.assertEqual(resposta_data['usuario'],self.usuario.username)
        self.assertEqual(resposta_data['treino'],treino.treino_nome)
        self.assertEqual(resposta_data['treino_id'],treino.id)
        self.assertEqual(resposta_data['videos'],esperando_video)
        self.assertEqual(resposta_data['ordem'],ordem)

    def test_treino_videos_cud_viewset_metodo_post_201_create_passando_treino_retorna_usuario_treino_treino_id_videos_ordem(self):
        # Criando um treino vinculado ao usuario authenticado
        treino = self.criar_treino(usuario=self.usuario)
        # Resposta id do treino ao usuario authenticado
        resposta = self.client.post(self.url,data={'treino':treino.id})
        resposta_data = resposta.data
        resposta_status = resposta.status_code
        
        self.assertEqual(resposta_status,HTTP_201_CREATED)
        self.assertEqual(len(resposta_data),6)
        
        # Testando retorno dos campos correspondente
        self.assertEqual(resposta_data['usuario'],self.usuario.username)
        self.assertEqual(resposta_data['treino'],treino.treino_nome)
        self.assertEqual(resposta_data['treino_id'],treino.id)
        self.assertEqual(resposta_data['videos'],[])
        self.assertEqual(resposta_data['ordem'],None)

    def test_treino_videos_cud_viewset_metodo_post_error_treino_nao_vinculado_ao_usuario(self):
        # Cirando um treino com novo usuario
        treino = self.criar_treino() 
        # Reposta id do treino do usuario diferente arguarda error
        resposta = self.client.post(self.url,data={'treino':treino.id})
        error_msg = resposta.data['treino'][0]
        error_esperado = f'Pk inválido "{treino.id}" - objeto não existe.'

        self.assertEqual(str(error_msg),error_esperado)
        self.assertEqual(error_msg.code,'invalid')
        self.assertEqual(resposta.status_code,HTTP_404_NOT_FOUND)

    def test_treino_videos_cud_viewset_metodo_patch_somente_vinculado_ao_usuario_codigo_200(self):
        video = self.criar_video(publicado=True)
        # Cliente autenticado
        _ , treino_video_usuario = self.criarTreinosVideos(self.usuario)
        # Cliente 2
        novo_usuario = self.cadastro_usuario('NewUser')
        treino_video_novo_usuario = self.criar_treino_videos(usuario=novo_usuario)
        # Resposta acessando ao pk vinculado ao usuario
        resposta = self.client.patch(f'{self.url}{treino_video_usuario.id}/',data={'videos':video.id})
        self.assertEqual(resposta.status_code,HTTP_200_OK)
        self.assertNotEqual(treino_video_usuario.id,treino_video_novo_usuario.id)

    def test_treino_videos_cud_viewset_metodo_patch_nao_vinculado_ao_usuario_retorna_codigo_404(self):
        video = self.criar_video(publicado=True)
        # Cliente autenticado criando treino videos
        self.criarTreinosVideos(self.usuario)
        # Cliente 2
        novo_usuario = self.cadastro_usuario('NewUser')
        treino_video_novo_usuario = self.criar_treino_videos(usuario=novo_usuario)
        # Resposta Acessando pk nao vinculado ao cliente autenticado
        resposta = self.client.patch(f'{self.url}{treino_video_novo_usuario.id}/',data={'videos':video.id})
        self.assertEqual(resposta.status_code,HTTP_404_NOT_FOUND)

    def test_treino_videos_cud_viewset_metodo_patch_retorna_campos_id_usuario_treino_treino_id_videos_ordem(self):
        video = self.criar_video(publicado=True)
        # Cliente authenticado criando treino videos
        treino , treino_video = self.criarTreinosVideos(usuario=self.usuario)
        resposta = self.client.patch(f'{self.url}{treino_video.id}/',data={'videos':video.id})
        resposta_data = resposta.data
        # Reposta
        self.assertEqual(resposta.status_code,HTTP_200_OK)
        self.assertEqual(len(resposta_data),6)
        self.assertEqual(resposta_data['id'],treino_video.id)
        self.assertEqual(resposta_data['usuario'],self.usuario.username)
        self.assertEqual(resposta_data['treino'],str(treino))
        self.assertEqual(resposta_data['treino_id'],treino.id)
        self.assertEqual(resposta.data['ordem'],None)

    def test_treino_videos_cud_viewset_metodo_patch_retorna_campos_videos_permitidos(self):
        video = self.criar_video(publicado=True)
        # Cliente authenticado criando treino videos
        treino , treino_video = self.criarTreinosVideos(usuario=self.usuario)
        resposta = self.client.patch(f'{self.url}{treino_video.id}/',data={'videos':video.id})
        resposta_data = resposta.data['videos'][0]
        # Campos permitidos para retorno
        campos_esperado = OrderedDict([('id_video', 1), 
                                       ('video_nome', 'Video Teste'), 
                                       ('video_id_youtube', 'iey118'), 
                                       ('video_url', 'https://www.youtube.com/embed/iey118'), 
                                       ('informacao', None), ('imagem', None), ('video_id_didatico', None), 
                                       ('grupo_muscular', 'Muscular'), ('equipamento', 'Equipamento')])
        self.assertEqual(resposta_data,campos_esperado)

    def test_treino_videos_cud_viewset_metodo_delete_nao_vinculado_ao_usuario_retorna_404(self):
        # CLiente authenticado
        _ , treino_video = self.criarTreinosVideos(usuario=self.usuario)
        
        # Cliente 2 
        novo_usuario = self.cadastro_usuario('New_user')
        treino_video_novo_usuario = self.criar_treino_videos(usuario=novo_usuario)
        # Resposta id usuario diferente
        resposta = self.client.delete(f'{self.url}{treino_video_novo_usuario.id}/')
        self.assertEqual(resposta.status_code,HTTP_404_NOT_FOUND)

    def test_treino_videos_cud_viewset_metodo_delete_nao_vinculado_ao_usuario_retorna_204(self):
        # CLiente authenticado
        _ , treino_video = self.criarTreinosVideos(usuario=self.usuario)
        # Reposta id usuario vinculado
        resposta = self.client.delete(f'{self.url}{treino_video.id}/')
        self.assertEqual(resposta.status_code,HTTP_204_NO_CONTENT)

    def test_treino_videos_cud_viewset_view_utilizar_get_publicado(self):
        # Videos 
        video_publicado_false = self.criar_video(publicado=False)
        video_publicado_true = self.criar_video(publicado=True)
        # Treino id
        treino  = self.criar_treino(usuario=self.usuario)

        dados_video_true = {
                            'treino':treino.id,
                            'videos':[video_publicado_true.pk],
                        }
        
        dados_video_False = {
            'treino':treino.id,
            'videos':[video_publicado_false.pk],
        }
        # Reposta videos publicado
        resposta_post_publicado = self.client.post(self.url,data=dados_video_true)
        
        self.assertEqual(resposta_post_publicado.status_code,HTTP_201_CREATED)
        
        # Reposta videos nao publicado
        resposta_post_nao_publicado = self.client.post(self.url,data=dados_video_False)
        
        self.assertEqual(resposta_post_nao_publicado.status_code,HTTP_400_BAD_REQUEST)
    