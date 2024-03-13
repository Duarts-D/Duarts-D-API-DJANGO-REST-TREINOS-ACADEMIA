from django.test import TestCase
from apps.academia.models import (EquipamentoModel,GrupoMuscularModel,VideoModel,
                                  TreinoModel,TreinoVideosmodel,TreinosCompartilhadosModel,
                                  )
from apps.academia.tests._utils_geradores_base import GeradoresBaseMixin
from django.contrib.auth.models import User
from django.urls import reverse
from pytest import raises


class UtilsGeradosBaseTest(TestCase):
    def setUp(self) -> None:
        self.gerador = GeradoresBaseMixin()
        self.usuario = User.objects.create_user(
            username='TestUserGeradores',
            email='TestEmail@email.com',
            password='TestUser123'
            )

    def test_geradores_base_criar_equipamento_sem_parametro_retorna_query_equipamento_equipamento(self):
        # Testa a funcao com parametro padrao
        equipamento = self.gerador.criar_equipamento()
        self.assertIsInstance(equipamento,EquipamentoModel)
        self.assertEqual(equipamento.equipamento , 'Equipamento')

    def test_geradores_base_criar_equipamento_com_parametro_barra_retorna_query_equipamento_barra(self):
        # Testa a funcao com parametro passado
        equipamento = self.gerador.criar_equipamento('barra')
        self.assertIsInstance(equipamento,EquipamentoModel)
        self.assertEqual(equipamento.equipamento , 'barra')

    def test_geradores_base_criar_grupo_muscular_sem_parametro_retorna_query_grupo_muscular_grupo(self):
        # Testa a funcao com parametro padrao
        grupo_muscular = self.gerador.criar_grupo_muscular()
        self.assertIsInstance(grupo_muscular,GrupoMuscularModel)
        self.assertEqual(grupo_muscular.grupo_muscular,'Grupo')

    def test_geradores_base_criar_grupo_muscular_com_parametro_ombros_retorna_query_grupo_muscular_ombros(self):
        # Testa a funcao com parametro padrao
        grupo_muscular = self.gerador.criar_grupo_muscular('Ombro')
        self.assertIsInstance(grupo_muscular,GrupoMuscularModel)
        self.assertEqual(grupo_muscular.grupo_muscular,'Ombro')
    
    def test_geradores_base_criar_video_sem_parametro_retorna_query_model(self):
        # Testa a funcao com parametro padrao
        video = self.gerador.criar_video()
        self.assertIsInstance(video,VideoModel)

    def test_geradores_base_criar_video_sem_parametro_retorna_model_EquipamentoModel_e_GrupoMuscularModel_da_instancia_correta(self):
        video = self.gerador.criar_video()
        # Models
        # model EquipamentoModel
        self.assertIsInstance(video.equipamento,EquipamentoModel)
        
        # model GrupoMuscularModel
        self.assertIsInstance(video.grupo_muscular,GrupoMuscularModel)
        
    def test_geradores_base_criar_video_com_parametro_retorna_query_model(self):
        # Testa a funcao com parametro passado
        nome = 'Video Teste'
        id_youtube = 'BaBa21y'
        grupo_muscular = 'Grupo teste'
        equipamento = 'Equipamento Teste'
        video = self.gerador.criar_video(
            video_nome=nome,
            video_id_youtube=id_youtube,
            grupo_muscular=grupo_muscular,
            equipamento=equipamento
        )
        
        # Campos
        self.assertEqual(video.video_nome,nome)
        self.assertEqual(video.video_id_youtube,id_youtube)
        self.assertEqual(video.grupo_muscular.grupo_muscular,grupo_muscular)
        self.assertEqual(video.equipamento.equipamento,equipamento)

        # Model
        self.assertIsInstance(video,VideoModel)

    def test_geradores_base_criar_video_com_parametro_retorna_model_EquipamentoModel_e_GrupoMuscularModel_da_instancia_correta(self):
        # Testa se a funcao esta criando para grupo muscular e o equipamento model passando os parametro a instância correta
        grupo_muscular = "Grupo Teste"
        equipamento = 'Equipamento Teste'
        video = self.gerador.criar_video(
            equipamento=equipamento,
            grupo_muscular=grupo_muscular
            )
        # Models
        # model EquipamentoModel
        self.assertIsInstance(video.equipamento,EquipamentoModel)
        self.assertEqual(video.equipamento.equipamento,equipamento)
        
        # model GrupoMuscularModel
        self.assertIsInstance(video.grupo_muscular,GrupoMuscularModel)
        self.assertEqual(video.grupo_muscular.grupo_muscular,grupo_muscular)
        
    def test_geradores_base_criar_treino_sem_parametro_criar_usuario_e_definir_padrao_nome_treino(self):
        # Testa a funcao com parametro padrao criar usuario
        
        # Quantidade de usuario antes da criacao 
        usuario = User.objects.count()
        # Quantidade de usuario cadastrado
        self.assertEqual(usuario,1)
        
        # Criando treino sem passar usuario
        treino = self.gerador.criar_treino()
        # Quantidade de usuario cadastrado
        usuarios = User.objects.count()
        self.assertEqual((usuario + 1),usuarios)

        # Nome padrao
        self.assertEqual(treino.treino_nome,'Treino')
    
    def test_geradores_base_criar_treino_retorna_instancia_de_TreinoModel(self):
        # Testa o retorno da funcao
        treino = self.gerador.criar_treino()
        # Model
        self.assertIsInstance(treino,TreinoModel)

    def test_geradores_base_criar_treino_passando_usuario_e_nome_treino(self):
        # Testa a funcao com usuario passando e nome do treino
        usuario = self.usuario
        nome_treino = 'Treino Test'
        treino = self.gerador.criar_treino(usuario=usuario,treino=nome_treino)
        self.assertIsInstance(treino,TreinoModel)
        self.assertEqual(treino.treino_nome, nome_treino)
        self.assertEqual(treino.usuario,usuario)
    
    def test_geradores_base_criar_treino_passando_nome_para_ser_criado_o_treino_associado(self):
        # Testa se esta criando um usuario com o nome passado
        nome_usuario = 'UsuarioTeste'
        treino = self.gerador.criar_treino(usuario=nome_usuario)
        usuario_treino = treino.usuario.username

        self.assertEqual(usuario_treino,nome_usuario)
        
    def test_geradores_base_criar_treinos_multiplicos_passando_quantideade_5_e_usuario_retornando_lista_de_instancia_treinoModel(self):
        #Testa a funcao retorna a quantidade 5 de Treinomodel
        usuario = self.usuario
        quantidade = 5 
        treinos = self.gerador.criar_treinos_multiplicos(qtd=quantidade,usuario=usuario)
        
        self.assertIsInstance(treinos,list)
        self.assertEqual(len(treinos),quantidade)

        for treino in treinos:
            self.assertIsInstance(treino,TreinoModel)
            self.assertEqual(treino.usuario,usuario)

    def test_geradores_base_criar_treinos_multiplicos_se_usuario_nao_for_instancia_userModel_retorna_error_valueError(self):
        # Testando se raise esta correto em relacao a instancia nao ser usermodel
        error_message = 'Usuario deve ser uma instancia de UserModel'
        with raises(ValueError) as msg_error:
            self.gerador.criar_treinos_multiplicos(qtd=5,usuario='da')
        # Verificando se messsage esta correta
        self.assertEqual(str(msg_error.value),error_message)

    def test_geradores_base_criar_videos_multiplicos_quantidade_5_retorna_lista_de_instancia_videosModel(self):
        #Testa a funcao retorna a quantidade 5 videoModel
        quantidade = 5 
        videos = self.gerador.criar_videos_multiplicos(qtd=quantidade)
        self.assertIsInstance(videos,list)
        self.assertEqual(len(videos),quantidade)
        
        # Verificando todas as instancia da lista
        for video in videos:
            self.assertIsInstance(video,VideoModel)

    def test_geradores_base_criar_treino_videos_retorna_uma_instancia_de_treinovideosmodel(self):
        # Testa o retorno da funcao
        treino_video  = self.gerador.criar_treino_videos()
        instancia = TreinoVideosmodel
        # Resposta
        self.assertIsInstance(treino_video,instancia)

    def test_geradores_criar_treino_videos_parametro_usuario_e_none_criar_um_usuario(self):
        # Testa se esta criando um usuario

        # Antes da funcao
        usuario_antes = User.objects.count()

        self.gerador.criar_treino_videos()
        # Depois da funcao
        usuarios_depois = User.objects.count() 
        self.assertEqual((usuario_antes+1),usuarios_depois)

    def test_geradores_criar_treino_videos_parametro_treino_e_none_retorna_intancia_com_treino_criado_com_nome_treino_associado(self):
        # Testa se esta criando um novo treino na funcao e utilizando
        treino_video = self.gerador.criar_treino_videos()    
        # Resposta
        self.assertIsInstance(treino_video,TreinoVideosmodel)
        self.assertEqual(treino_video.treino.treino_nome,'Treino')

    def test_geradores_criar_treino_videos_parametro_treino_e_str_treinoteste_retorna_intancia_vinculado_ao_treino_criado_treinoteste(self):
        # Testa se esta criando treino com parametro str informado
        treino_str = 'TreinoTeste'
        treino_video = self.gerador.criar_treino_videos(treino=treino_str)
        # Resposta
        self.assertEqual(treino_video.treino.treino_nome,treino_str)

    def test_geradores_criar_treino_videos_parametro_treino_instancia_de_usuario_diferente_retorna_raise_valueerror(self):
        # Testa o raise levatado quando treino e diferente do usuario
        # Criando usuario e associando um treino
        usuario = self.gerador.cadastro_usuario('UserTestTreinoVideos')
        treino_nome = 'Treino do teste raise'
        treino = self.gerador.criar_treino(treino=treino_nome,usuario=usuario)
        # Resposta 
        # Levantara o erro quando a instancia do treino nao for do usuario
        with raises(ValueError) as error_raise_msg:
            self.gerador.criar_treino_videos(treino=treino)
        msg_error_esperado = 'O Usuario e treino nao estão associados.'
        # Verificando msg de error
        self.assertEqual(str(error_raise_msg.value),msg_error_esperado)

    def test_geradores_criar_treino_videos_parametro_videos_nao_for_passado_criar_um_video(self):
        # Testa a criacao de 1 video associado ao treino_videos
        treino_videos = self.gerador.criar_treino_videos()
        quantidade_videos = treino_videos.videos.count()
        esperado = 1 
        # Resposta 
        self.assertEqual(quantidade_videos,esperado)

    def test_geradores_base_criar_treino_videos_parametro_videos_passado_lista_com_3_videos_retornando_quantidade_de_3_videos(self):
        # Criar lista de videos
        videos_lista = self.gerador.criar_videos_multiplicos(qtd=3)
        
        # Criar Treinovideos
        treino_videos = self.gerador.criar_treino_videos(videos=videos_lista)
        quantidade_treino_videos = treino_videos.videos.count()
        
        # Resposta
        # Quantidade associada aos treinoVideos
        self.assertEqual(quantidade_treino_videos,len(videos_lista))
        # verifica se os videos salvo sao os mesmo
        self.assertEqual(list(treino_videos.videos.all()),videos_lista)
        
    def test_geradores_base_criar_treino_videos_parametro_videos_nao_e_uma_lista_retorna_raise_valueerror(self):
        videos_tupl = ('b',)
        # Reposta raise
        with raises(ValueError) as raise_error_msg:
            self.gerador.criar_treino_videos(videos=videos_tupl)
        # Erro raise msg
        esperando_msg = ('Videos deve ser uma "lista" de instancia de VideosModel.')
        self.assertEqual(str(raise_error_msg.value),esperando_msg)
    
    def test_geradores_base_criar_treino_video_parametro_videos_lista_nao_instancia_de_VideoModel_retorna_valueerror(self):
        # Videos
        instancia_1 = self.gerador.criar_equipamento() # Instancia de EquipamentoModel
        instancia_2 = self.gerador.criar_grupo_muscular() # instancia de GrupoMuscular
        videos_lista = [instancia_1,instancia_2]
        # Reposta
        with raises(TypeError) as raise_error_msg:
            self.gerador.criar_treino_videos(videos=videos_lista)
        # Error raise msg
        esperando_msg = ('Video deve ser uma "instancia de VideoModel"')
        self.assertEqual(str(raise_error_msg.value),esperando_msg)

    def test_criar_treino_compartilhado_default(self):
        esperado = 'Treino'
        resposta = self.gerador.criar_treino_compartilhado()
        assert esperado == resposta.treino

    def test_criar_treino_compratilhado_return_instancia_treinocompartilhadomodel(self):
        esperado_model = TreinosCompartilhadosModel
        resposta = self.gerador.criar_treino_compartilhado()
        assert isinstance(resposta,esperado_model)

    def test_criar_treino_compartilhado_param_treino(self):
        esperado = 'Treinos'
        resposta = self.gerador.criar_treino_compartilhado(treino=esperado)
        assert resposta.treino == esperado

    def test_url_retrieve_defaul(self):
        url = 'compartilhar-retrieve'
        esperado = '/c-retrieve/abc/'
        resposta = self.gerador.url_retrieve_slug(url=url)
        assert resposta == esperado

    def test_url_retrieve_retorna_url_com_slug(self):
        url = 'compartilhar-retrieve'
        slug = 'slug_compartilhado'
        esperado = f'/c-retrieve/{slug}/'
        resposta = self.gerador.url_retrieve_slug(url=url,slug=slug)
        assert resposta == esperado

class UtilsGeradosBaseClientTest(GeradoresBaseMixin,TestCase):
    def test_geradores_base_criar_logout_logar_sem_parametros_esta_criando_usuario_e_logando(self):
        # Testa se esta criando usuario corretamente e esta logando
        username , cadastro = self.criar_usuario_logout_logar()

        # Resposta
        url = reverse('treino-listas-list')
        resposta = self.client.get(url)
        status = 200
        
        # Verifica se o usuario esta criado
        self.assertIsNotNone(cadastro)
        self.assertIsInstance(cadastro,User)

        # Verifica se esta logado
        self.assertEqual(resposta.status_code,status)
        self.assertIsInstance(username,str)
        

