from apps.academia.views import VideosViewList
from apps.academia.models import VideoModel
from django.urls import resolve,reverse
from apps.academia.tests._utils_geradores_base import GeradoresBaseMixin
from pytest import mark
from apps.academia.serializers import VideosSerializer
from rest_framework.status import HTTP_200_OK,HTTP_405_METHOD_NOT_ALLOWED


class TestVideosViewListFunc(GeradoresBaseMixin):
    """ Testes da view VideosViewFunc"""

    def test_videos_view_list_view_func(self):
        # Testando a funcao utilizando na view
        url = 'videos-list'
        func = VideosViewList
        resultado = resolve(self.url_retrieve(url=url))
        assert resultado.func.view_class == func

    @mark.django_db
    def test_videos_view_list_retorna_query_com_videos_publicado(self,videos_factory):
        videos_publicado = videos_factory.create_batch(5,publicado=True)
        videos_nao_publicado = videos_factory.create_batch(3,publicado=False)
        resultado = VideosViewList().queryset
        assert len(resultado) == 5
        videos_total = VideoModel.objects.all()
        assert len(videos_total)  == 8
    
    def test_videos_view_list_serializer(self):
        resultado = VideosViewList().serializer_class
        assert resultado == VideosSerializer

    def test_videos_view_list_authentication_nenhuma(self):
        resultado = VideosViewList().authentication_classes
        assert resultado == []
    
    def test_videos_view_list_permission_nenhuma(self):
        resultado = VideosViewList().permission_classes
        assert resultado == []

@mark.django_db
class TestVideosViewListCliente:
    """ Testes da view VideosView"""
    def test_videos_view_list_get_retornar_status_200(self,url_videos,cliente_user):
        # Testando metodo get 
        resultado = cliente_user.get(url_videos)
        assert resultado.status_code == HTTP_200_OK
        
    def test_videos_view_list_post_retornar_status_405(self,url_videos,cliente_user):
        # Testando se metodo post bloqueado
        resultado = cliente_user.post(url_videos)
        assert resultado.status_code == HTTP_405_METHOD_NOT_ALLOWED

    def test_videos_view_list_patch_retornar_status_405(self,url_videos,cliente_user):
        # Testando se metodo patch bloqueado
        resultado = cliente_user.patch(url_videos)
        assert resultado.status_code == HTTP_405_METHOD_NOT_ALLOWED

    def test_videos_view_list_put_retornar_status_405(self,url_videos,cliente_user):
        # Testando se metodo put bloqueado
        resultado = cliente_user.put(url_videos)
        assert resultado.status_code == HTTP_405_METHOD_NOT_ALLOWED

    def test_videos_view_list_delete_retornar_status_405(self,url_videos,cliente_user):
        # Testando se metodo delete bloqueado
        resultado = cliente_user.delete(url_videos)
        assert resultado.status_code == HTTP_405_METHOD_NOT_ALLOWED

    def test_videos_view_list_retorna_lista_de_videos_publicado(self,url_videos,cliente_user,videos_factory):
        # Testando se retorna lista de videos publicado 
        videos_5 = videos_factory.create_batch(5,publicado=True)
        videos_3 = videos_factory.create_batch(5,publicado=False)

        resultado = cliente_user.get(url_videos)
        assert len(resultado.data) == 5

        resultado = resultado.data
        for i , video in enumerate(videos_5):
            assert video.id == resultado[i]['id_video']
            assert video.video_nome == resultado[i]['video_nome']

    def test_videos_view_list_retorna_campos(self,cliente_user_videos_get):
        resultado = cliente_user_videos_get.data[0]
        esperado_video_db = VideoModel.objects.get(publicado=True,id=resultado['id_video'])
        
        # Retornado somente 1 query
        assert len(cliente_user_videos_get.data) == 1
        # Quantidade de keys retornado
        assert len(resultado) == 9
        # Verificando os campos
        assert resultado['id_video']  == esperado_video_db.id
        assert resultado['video_nome']  == esperado_video_db.video_nome
        assert resultado['video_id_youtube']  == esperado_video_db.video_id_youtube 
        assert resultado['video_url']  == esperado_video_db.video_url 
        assert resultado['informacao']  == esperado_video_db.informacao 
        assert resultado['imagem']  == None if not esperado_video_db.imagem.name else esperado_video_db.imagem.name
        assert resultado['video_id_didatico']  == esperado_video_db.video_id_didatico 
        assert resultado['grupo_muscular']  == esperado_video_db.grupo_muscular.__str__()
        assert resultado['equipamento']  == esperado_video_db.equipamento.__str__()

    def test_videos_view_list_query_params_equipamento_retorna_lista_com_videos_com_equipamento_barra(self,url_videos,videos_factory,cliente_user):
        # Testando o retorno  da query do params equipamento
        equipamento = 'Barra'
        videos = videos_factory.create_batch(2,publicado=True,equipamento__equipamento=equipamento)
        video_2 = videos_factory.create(publicado=True,equipamento__equipamento='<Rosca>')

        url = url_videos + f'?equipamentos={equipamento}'
        resposta = cliente_user.get(url).data

        assert len(resposta) == 2
        assert resposta[0]['id_video'] == videos[0].id
        assert resposta[1]['id_video'] == videos[1].id

    def test_videos_view_list_query_params_equipamento_nao_existente_retorna_lista_vazia(self,url_videos,videos_factory,cliente_user):
        # Testando o retorno do equipamento nao existente
        equipamento = 'Agua'
        
        videos_factory.create_batch(2,publicado=True,equipamento__equipamento='barra')
        videos_factory.create(publicado=True,equipamento__equipamento='<Rosca>')

        url = url_videos + f'?equipamentos={equipamento}'
        resposta = cliente_user.get(url).data
        assert len(resposta) == 0
    
    def test_videos_view_list_query_params_grupo_muscular_retorna_lista_com_grupo_muscular_superiro(self,url_videos,videos_factory,cliente_user):
        # testando o retorno da query do params grupo_muscular
        grupo_muscular = 'Superior'
        
        videos = videos_factory.create_batch(2,publicado=True,grupo_muscular__grupo_muscular=grupo_muscular)
        videos_factory.create(publicado=True,grupo_muscular__grupo_muscular='<inferior>')

        url = url_videos + f'?grupos={grupo_muscular}'
        resposta = cliente_user.get(url).data
        
        assert len(resposta) == 2
        assert resposta[0]['id_video'] == videos[0].id
        assert resposta[1]['id_video'] == videos[1].id

    def test_videos_view_list_query_params_grupo_muscular_nao_existe_retorna_lista_vazia(self,url_videos,videos_factory,cliente_user):
        # Testando o retorno do grupo_muscular nao existente
        grupo_muscular = 'grupos'
        
        videos_factory.create_batch(2,publicado=True,grupo_muscular__grupo_muscular='Superior')
        videos_factory.create(publicado=True,grupo_muscular__grupo_muscular='<inferior>')

        url = url_videos + f'?grupos={grupo_muscular}'
        resposta = cliente_user.get(url).data
        
        assert len(resposta) == 0

    def test_videos_view_list_query_params_video_str_retorna_videos(self,url_videos,cliente_user,videos_factory):
        # Testando o retorno de videos com nome
        video = 'Afundo'
        video_0 = videos_factory.create(video_nome=video)
        video_1 = videos_factory.create(video_nome=f'lungues-{video}')  
        video_2 = videos_factory.create(video_nome=f'{video}-halter')  
        video_3 = videos_factory.create(video_nome=f'rosca-{video}-vertical')  
        videos = videos_factory.create_batch(3)

        url = url_videos + f'?videos={video}'
        resultado = cliente_user.get(url).data
        assert len(resultado) == 4
        assert video_0.id == resultado[0]['id_video']
        assert video_1.id == resultado[1]['id_video']
        assert video_2.id == resultado[2]['id_video']
        assert video_3.id == resultado[3]['id_video']

    def test_videos_view_list_query_params_agrupamentos_de_consulta(self,url_videos,videos_factory,cliente_user):
        # Testand consulta com agrupamentos
        video = 'Afundo'
        equipamento = 'barra'
        grupo_muscular = 'Superior'
        # Videos
        video_0 = videos_factory.create(video_nome=video)
        video_1 = videos_factory.create(
            video_nome=f'{video}-primeiro',
            equipamento__equipamento=equipamento,
            grupo_muscular__grupo_muscular=grupo_muscular
        )
        video_2 = videos_factory.create(
            video_nome=f'final-{video}',
            equipamento__equipamento=equipamento,
            grupo_muscular__grupo_muscular=grupo_muscular
        )
        videos_factory.create_batch(5)
        
        # Lista de videos 
        lista_model_videos = [video_0, video_1, video_2]
        lista_model_equip_grup = [video_1,video_2]
        
        # Resposta 1 retorna os 3 videos
        url_video = url_videos + f'?videos={video}'
        resposta_0 = cliente_user.get(url_video).data
        assert len(resposta_0) == 3
        for i , resposta in enumerate(resposta_0):
            assert resposta['id_video'] == lista_model_videos[i].id

        # Resposta 2 retorna somente 2 videos
        url_vid_equip_grup = url_videos + f'?videos={video}&equipamento={equipamento}&grupos={grupo_muscular}'
        resposta_1 = cliente_user.get(url_vid_equip_grup).data
        
        assert len(resposta_1) == 2

        lista_id = list(map(lambda x : x.id, lista_model_equip_grup))
        for resposta in resposta_1:
            assert resposta['id_video'] in lista_id

        # Total de videos salvo no banco de dados para garantir que esta voltando somente necessario
        instancias = VideoModel.objects.all()
        assert instancias.count() == 8 