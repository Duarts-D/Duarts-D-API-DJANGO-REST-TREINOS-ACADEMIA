from apps.academia.models import (VideoModel,EquipamentoModel,GrupoMuscularModel,
                                  TreinoModel,TreinoVideosmodel)
from apps.usuarios.tests.test_cadastro_base import CadastroMixin
from django.contrib.auth.models import User

class GeradoresBaseMixin(CadastroMixin):
    """
    -> Sistema de geradores de instância de model para utilizar nos testes.
    """

    def criar_equipamento(self,nome: str ='Equipamento'): 
        """
        -> Cria um instância do modelo EquipamentoModel .

        :param nome: (str) O nome do equipamento a ser criado. (opcional, padrão: 'Equipamento')
        :return: Instância do modelo EquipamentoModel criado. 
        """
        return EquipamentoModel.objects.create(equipamento=nome)
    
    def criar_grupo_muscular(self,nome='Grupo'):
        """
        -> Cria um instância do modelo GrupoMuscularModel .

        :param nome: (str) O nome do grupo muscular a ser criado. (opcional, padrão: 'Grupo')
        :return: Instância do modelo GrupoMuscularModel criado. 
        """
        return GrupoMuscularModel.objects.create(grupo_muscular=nome)

    def criar_video(self,
               video_nome='Video Teste',
               video_id_youtube='iey118',
               grupo_muscular = 'Muscular',
               equipamento = 'Equipamento',
               publicado = False
               ):
        """
        Cria uma nova instância do modelo VideoModel.

        :param video_nome: (str) O nome do vídeo a ser criado. (opcional, padrão: 'Video Teste')
        :param video_id_youtube: (str) O ID do vídeo no YouTube a ser criado. (opcional, padrão: 'iey118')
        :param grupo_muscular: (str) O nome do grupo muscular associado ao vídeo. (opcional, padrão: 'Muscular')
        :param equipamento: (str) O nome do equipamento associado ao vídeo. (opcional, padrão: 'Equipamento')
        :return: Instância do modelo VideoModel criada.
        """

        return VideoModel.objects.create(
            video_nome = video_nome,
            video_id_youtube=video_id_youtube,
            grupo_muscular = self.criar_grupo_muscular(nome=grupo_muscular),
            equipamento = self.criar_equipamento(nome=equipamento),
            publicado=publicado
        )
    
    def criar_treino(self,treino='Treino',usuario=None):
        """
        -> Criar um treino e vincula ao usuario.
        
        :param treino: (str) O nome do treino a ser criado. (opcional, padrão:'Treino')
        :param usuario: (UserModel) | (str) O usuario a ser associado ou criado, se nao for passado sera criado um novo usuario.(opcional, padrão:None) 
        :return: Instância do modelo TreinoModel 

        """
        
        if not isinstance(usuario,User):
            usuario = 'TestUser' if usuario is None else usuario
            usuario = self.cadastro_usuario(username=usuario)

        return TreinoModel.objects.create(
            usuario = usuario,
            treino_nome = treino
        )
    
    def criar_treinos_multiplicos(self,qtd:int,usuario=User):
        """
        -> Cria quantidade específica de instância de TreinoModel vinculado ao usuario.

        :param qtd: (int) Quantidade de treinos a ser criado.
        :param usuario: (UserModel) Usuario a se associado os treinos.
        :return: Lista de instância do modelo TreinoModel criado.        
        """

        if not isinstance(usuario,User):
            raise ValueError('Usuario deve ser uma instancia de UserModel')
        
        lista = []
        for k in range(qtd):
            nome = f'treino_{k}'
            treino = self.criar_treino(treino=nome,usuario=usuario)
            lista.append(treino)
        return lista

    def criar_videos_multiplicos(self,qtd:int):
        """
        -> Cria quantidade específica de instância de VideoModel. 
        
        :param qtd: (int) Quantidade de videos a ser criado.
        :return: Uma lista com instâncias criada do modelo VideoModel.
        """
        lista = []
        for _ in range(qtd):
            lista.append(self.criar_video(publicado=True))
        return lista

    def criar_usuario_logout_logar(self,
                                   username='Cliente',
                                   password='userTest123'
                                   ):
        """
        -> Cria um usuário se nao estiver cadastrado, 
        faz logout se já houver um usuário logado e faz login com as credenciais fornecidas.
        
        :param username: (str) O nome do usuario a ser criado . (opcional, padrão: 'Cliente')
        :param password: (str) A senha do usuario a ser criado . (opcional, padrão: 'userTest123')
        :return: Tupla contendo o nome do usuario e a instância do modelo User.
        """
        usuario = User.objects.filter(username=username).first()
        if not usuario:
            usuario = self.cadastro_usuario(username=username,password=password)
        
        self.client.logout()
        self.client.login(
            username=username, 
            password=password)
        
        return username,usuario

    def criar_treino_videos(self,usuario:User=None,treino:TreinoModel=None,videos=[]):
        """
        -> Cria uma instância de TreinoVideosModel e associa vídeos e treino a ele,
        adicionando ao usuário especificado ou criando um novo usuário se não for passado.

        :param usuario: (UserModel) O Usuario a ser associado na instâncias. Se nao for passado, um novo usuario sera criado.(opcional, padrão: None)
        :param treino: (TreinoModel) | (str) O treino ao qual os videos vao ser associado na instância. Se nao for passado , um novo treino sera criado,
                        pode-se passar o nome do treino para criacao.
                        Deve pertencer ao usuario passado como parametro. (opcional, padrão: None)
        :param videos: (list) Uma lista de instância do modelo VideoModel, se nao for passado, um novo video sera criado e associado ao TreinoVideosModel
        :return: Instância do modelo TreinoVIdeosModel criado.
        """

        # Cadastra novo usuario se nao for passado UserModel
        if usuario is None:
            usuario = self.cadastro_usuario()
        
        # Verifica se treino e uma instancia de TreinoModel
        if not isinstance(treino,TreinoModel):
            treino_name = 'Treino' if treino is None else treino
            treino = self.criar_treino(usuario=usuario,treino=treino_name)    
        else:
            # Verifica se o treino passado esta vinculado ao usuario
            if not treino.usuario == usuario:
                raise ValueError('O Usuario e treino nao estão associados.')
        
        # Cria a instancia TreinoVideosModel
        treino_video = TreinoVideosmodel.objects.create(
            usuario = usuario,
            treino = treino,
        )
        # Verifica se a lista de video esta vazia , e cria uma lista com 1 video
        if not isinstance(videos,list):
            raise ValueError('Videos deve ser uma "lista" de instancia de VideosModel.')
        if not videos:
            video = self.criar_video(publicado=True)
            videos = [video,]
        else:
            for video in videos:
                if not isinstance(video,VideoModel):
                    raise TypeError('Video deve ser uma "instancia de VideoModel"')
        # Associa os video a instância de TreinoVideosModel criada 
        treino_video.videos.set(videos)
        treino_video.save()
        
        return treino_video