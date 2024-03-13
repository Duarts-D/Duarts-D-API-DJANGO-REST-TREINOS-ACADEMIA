import pytest
from rest_framework.test import APIClient
from ._utils_geradores_base import GeradoresBaseMixin
from apps.academia.tests.factories import TreinoCompartilhadoFactory,VideosFactory
from pytest_factoryboy import register
from apps.academia import models
from random import randint
from apps.academia import serializers

register(TreinoCompartilhadoFactory)


@pytest.fixture
def url_add(geradores):
    return geradores.url_retrieve('compartilhar-add') 

@pytest.fixture
def treino_compartilhado():
    return TreinoCompartilhadoFactory()


@pytest.fixture
def treino_compartilhado_com_videos():
    treino = TreinoCompartilhadoFactory.create(videos=(VideosFactory(), VideosFactory(), VideosFactory()))
    return treino


@pytest.fixture
def treino_compartilhado_add_criado(geradores,treino_compartilhado_com_videos,cliente_user):
    """
    -> Criar um treino compartilhado atraves do post de compartilhar-add.
    
    :return: retorna o cliente utilizado para requisicao e treino compartilhado criado.
    """
    slug = treino_compartilhado_com_videos.slug
    dados = {'slug_compartilhado': slug }
    url = geradores.url_retrieve('compartilhar-add')
    resposta_cliente = cliente_user.post(url,data=dados)
    return resposta_cliente , treino_compartilhado_com_videos

@pytest.fixture
def treino_compartilhado_add_criando_2(geradores,treino_compartilhado_com_videos,cliente_user):
    slug = treino_compartilhado_com_videos.slug
    dados = {'slug_compartilhado': slug }
    url = geradores.url_retrieve('compartilhar-add')
    resposta_1 = cliente_user.post(url,data=dados)
    resposta_2 = cliente_user.post(url,data=dados)
    return resposta_1 , resposta_2

@pytest.fixture()
def treino_compartilhado_e_treino_videos_criado_na_view_TreinoCompartilhadoAdd(treino_compartilhado_add_criado):
    _ , treino_compartilhado_com_videos = treino_compartilhado_add_criado
    treino_videos = models.TreinoVideosmodel.objects.get(slug_compartilhado=treino_compartilhado_com_videos.slug)
    return treino_videos , treino_compartilhado_com_videos 

@pytest.fixture
def client():
    cliente = APIClient()
    return cliente

@pytest.fixture
def geradores():
    gerador = GeradoresBaseMixin()
    return gerador

@pytest.fixture
def cliente_user(geradores,client):
    username = 'ClienteUser'
    senha = 'UserCliente'
    geradores.cadastro_usuario(username=username,password=senha)
    client.login(username=username,password=senha)
    return client

@pytest.fixture
def criando_5_model_treino_compartilhado_com_requisicao(treino_compartilhado_factory,cliente_user,url_add):
    qtd_treino_repetido = 5
    for _ in range(0,qtd_treino_repetido ):
        treino_compartilhado = treino_compartilhado_factory.create(treino='Treino-repetido',slug=f'Treino-repetido-{randint(1,1000)}')
        dados = {'slug_compartilhado': treino_compartilhado.slug }
        cliente_user.post(url_add,data=dados)

@pytest.fixture
def serializer_add_compartilhado():
    serializer = serializers.TreinoCompartilhadoSerializerAdd()
    return serializer