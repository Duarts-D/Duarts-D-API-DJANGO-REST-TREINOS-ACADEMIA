from apps.academia.models import (VideoModel,EquipamentoModel,GrupoMuscularModel,
                                  TreinoModel)
from apps.usuarios.tests.test_cadastro_base import CadastroMixin

class Geradores_base_mixin(CadastroMixin):
    def criar_equipamentos(self,equipamento='Equipamento'):
        return EquipamentoModel.objects.create(equipamento=equipamento)
    
    def criar_grupo_muscular(self,grupo_muscular='Grupo'):
        return GrupoMuscularModel.objects.create(grupo_muscular=grupo_muscular)

    def criar_video(self,
               video_nome='Video Teste',
               video_id_youtube='iey118',
               grupo_muscular = 'Muscular',
               equipamento = 'Equipamento'
               ):
        return VideoModel.objects.create(
            video_nome = video_nome,
            video_id_youtube=video_id_youtube,
            grupo_muscular = self.criar_grupo_muscular(grupo_muscular=grupo_muscular),
            equipamento = self.criar_equipamentos(equipamento=equipamento)
        )
    
    def criar_treino(self,treino='Treino'):
        return TreinoModel.objects.create(
            usuario = self.cadastro_usuario(),
            treino_nome = treino
        )

    def videos_multiplicos(self,qtd):
        lista = []
        for _ in range(qtd):
            lista.append(self.criar_video())
        return lista
