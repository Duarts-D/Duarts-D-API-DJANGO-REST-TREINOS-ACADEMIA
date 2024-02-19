from django.test import TestCase
from apps.academia.models import (VideoModel,GrupoMuscularModel,EquipamentoModel,
                                  TreinoModel,TreinoVideosmodel)
from django.contrib.auth.models import User
from apps.usuarios.tests.test_cadastro_base import CadastroMixin
from apps.academia.tests.utils_geradores_base import GeradoresBaseMixin
from pytest import raises
from django.db import IntegrityError

class VideoModelTest(TestCase):
    def test_videomodel_esta_salvando_url_corretamente_com_os_parametro_inicial_do_youtube(self):
        video_id_youtube = 'abc54brca1'
        video = VideoModel.objects.create(
            video_nome = 'Video teste',
            video_id_youtube= video_id_youtube
        )
        video_salvo = VideoModel.objects.get(id=video.id)
        esperado = 'https://www.youtube.com/embed/'+ video_id_youtube
        self.assertEqual(video_salvo.video_url,esperado)

    def test_videomodel_integracao_ForeignKey_grupo_muscular_e_equipamento(self):
        grupo_muscular = GrupoMuscularModel.objects.create(grupo_muscular='Grupo teste')
        equipamento = EquipamentoModel.objects.create(equipamento='Aparelho teste')

        video = VideoModel.objects.create(
            video_nome = 'Video teste',
            video_id_youtube = 'ab1T12se',
            grupo_muscular = grupo_muscular,
            equipamento = equipamento
        )
        video.save()

        resposta = VideoModel.objects.get(id=video.id)

        self.assertEqual(resposta.grupo_muscular,grupo_muscular)
        self.assertEqual(resposta.equipamento,equipamento)

class TreinoModelTest(CadastroMixin,TestCase):
    def test_treino_model_integridade_de_forekey(self):
        user = self.cadastro_usuario()
        TreinoModel.objects.create(
            usuario = user,
            treino_nome = 'Treino'
        )
        respota = TreinoModel.objects.get(usuario=user)
        self.assertEqual(respota.treino_nome,"Treino")
        self.assertEqual(respota.usuario, user)
        
    def test_treino_model_usario_e_treino_nome_unicos_juntos(self):
        usuario_1 = self.cadastro_usuario()
        usuario_2 = self.cadastro_usuario(username='Usuario2')

        nome_treino = 'treino_teste'
        
        treino_1 = TreinoModel.objects.create(usuario=usuario_1,treino_nome=nome_treino)
        treino_2 = TreinoModel.objects.create(usuario=usuario_2,treino_nome=nome_treino)
        
        self.assertEqual(treino_1.treino_nome,nome_treino)
        self.assertEqual(treino_2.treino_nome,nome_treino)

        with raises(IntegrityError) as msg_error:
            TreinoModel.objects.create(usuario=usuario_1,treino_nome=nome_treino)
        msg_esperada = 'UNIQUE constraint failed:'
        self.assertIn(msg_esperada,str(msg_error.value))
        


class TreinoVideosModelTest(GeradoresBaseMixin,CadastroMixin,TestCase):
    def test_treino_videos_model_itegridade_de_forekey(self):
        user = self.cadastro_usuario(username='TesteTreino')
        treino = self.criar_treino()
        videos = self.criar_videos_multiplicos(5)
        treinovideos = TreinoVideosmodel.objects.create(
            usuario=user,
            treino=treino
        )
        treinovideos.videos.set(videos)
        treinovideos.save()

        resposta_criado_viculado = TreinoVideosmodel.objects.filter(usuario=user).exists()
        resposta_treino_viculado = TreinoVideosmodel.objects.filter(treino=treino).exists()        
        self.assertTrue(resposta_criado_viculado)
        self.assertTrue(resposta_treino_viculado)

        resposta_videos = TreinoVideosmodel.objects.get(usuario=user)
        resposta_videos = list(resposta_videos.videos.all())
        self.assertEqual(resposta_videos,videos)

    def test_treino_videos_model_usario_e_treino_nome_unicos_juntos(self):
        usuario_1 = self.cadastro_usuario(username='Usuario_1')
        usuario_2 = self.cadastro_usuario(username='Usuario_2')
        nome_treino = 'Treino_testando'
        treino_1 = TreinoModel.objects.create(usuario=usuario_1,treino_nome=nome_treino)
        treino_2 = TreinoModel.objects.create(usuario=usuario_2,treino_nome=nome_treino)

        TreinoVideosmodel.objects.create(
            usuario=usuario_1,
            treino = treino_1,
        )

        TreinoVideosmodel.objects.create(
            usuario=usuario_2,
            treino = treino_2,
        )
        quantidade_treinos_videos = TreinoVideosmodel.objects.count()
        self.assertEqual(quantidade_treinos_videos, 2 )

        with raises(IntegrityError) as error_msg:
            TreinoVideosmodel.objects.create(
                usuario=usuario_2,
                treino = treino_2,
            )
        msg_erro = str(error_msg.value)
        msg_esperada = 'UNIQUE constraint failed:'
        self.assertIn(msg_esperada, msg_erro)