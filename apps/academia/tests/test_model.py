from django.test import TestCase
from apps.academia.models import VideoModel,GrupoMuscularModel,EquipamentoModel
from django.contrib.auth.models import User

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