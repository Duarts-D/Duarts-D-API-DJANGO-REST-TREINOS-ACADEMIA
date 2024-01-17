from django.test import TestCase
from apps.academia.models import (VideoModel,GrupoMuscularModel,EquipamentoModel,
                                  TreinoModel,TreinoVideosmodel)
from django.contrib.auth.models import User
from apps.usuarios.tests.test_cadastro_base import CadastroMixin
from apps.academia.tests.test_geradores_base import Geradores_base_mixin

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
        

class TreinoVideosModelTest(Geradores_base_mixin,CadastroMixin,TestCase):
    def test_treino_videos_model_itegridade_de_forekey(self):
        user = self.cadastro_usuario(username='TesteTreino')
        treino = self.criar_treino()
        videos = self.videos_multiplicos(5)
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