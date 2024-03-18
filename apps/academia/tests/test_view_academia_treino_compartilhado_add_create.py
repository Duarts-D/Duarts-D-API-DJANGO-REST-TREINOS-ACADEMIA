from rest_framework.status import (HTTP_405_METHOD_NOT_ALLOWED,HTTP_201_CREATED,
                                   HTTP_401_UNAUTHORIZED,HTTP_400_BAD_REQUEST,)
from apps.academia.tests._utils_geradores_base import GeradoresBaseMixin
from django.urls import resolve
from apps.academia import models 
from apps.academia.views import TreinoCompartilhadoAddViewCreate
from apps.academia.serializers import TreinoCompartilhadoSerializerAdd
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated
import pytest
from unittest.mock import patch
from apps.academia import models
from apps.academia.views import QTD_TREINO_REPETIDO
from django.db.utils import IntegrityError
from pytest import raises

class TestTreinoCompartilhadoAddViewFunc(GeradoresBaseMixin):
    """ Testes da view TreinoCompartilhadoAddFunc"""
    def test_treino_compartilhado_add_view_func(self):
        # Testando a funcao utilizando na view
        url = 'compartilhar-add'
        func = TreinoCompartilhadoAddViewCreate
        resultado = resolve(self.url_retrieve(url=url))
        assert resultado.func.view_class == func

    def test_treino_compartilhado_add_serializer_class_e_treino_compartilhado_add_serializer(self):
        # Testando o serializer utilizado
        esperado = TreinoCompartilhadoSerializerAdd
        resultado = TreinoCompartilhadoAddViewCreate().serializer_class

        assert resultado == esperado

    def test_treino_compartilhado_add_permission_class(self):
        # Testando as permisao necessaria
        esperado = [IsAuthenticated]
        resultado = TreinoCompartilhadoAddViewCreate().permission_classes

        assert resultado == esperado

    def test_treino_compartilhado_add_authentication_classe(self):
        # Testand oas authenticacao necessaria
        esperado = [BasicAuthentication, SessionAuthentication]
        resultado = TreinoCompartilhadoAddViewCreate().authentication_classes

        assert resultado == esperado

@pytest.mark.django_db
class TestTreinoCompartilhadoAddViewClient(GeradoresBaseMixin):
    """ Testes da view TreinoCompartilhadoAdd"""
    def setup_method(self) :
        self.url = 'compartilhar-add'

    def test_treino_compartilhado_add_get_retorna_status_405(self,cliente_user):
        # Testando se metodo get bloqueado
        resultado = cliente_user.get(self.url_retrieve(url=self.url))

        assert resultado.status_code == HTTP_405_METHOD_NOT_ALLOWED

    def test_treino_compartilhado_add_get_kwargs_retorna_status_405(self,cliente_user):
        # Testando se metodo get pk bloqueado
        resultado = cliente_user.get(self.url_retrieve(url=self.url))

        assert resultado.status_code == HTTP_405_METHOD_NOT_ALLOWED

    def test_treino_compartilhado_add_delete_retorna_status_405(self,cliente_user):
        # Testando se metodo delete bloqueado
        resultado = cliente_user.delete(self.url_retrieve(url=self.url))

        assert resultado.status_code == HTTP_405_METHOD_NOT_ALLOWED

    def test_treino_compartilhado_add_patch_retorna_status_405(self,cliente_user):
        # Testando se metodo patch bloqueado
        resultado = cliente_user.patch(self.url_retrieve(url=self.url))

        assert resultado.status_code == HTTP_405_METHOD_NOT_ALLOWED
        
    def test_treino_compartilhado_add_put_retorna_status_405(self,cliente_user):
        # Testando se metodo put bloqueado
        resultado = cliente_user.put(self.url_retrieve(url=self.url))
       
        assert resultado.status_code == HTTP_405_METHOD_NOT_ALLOWED

    def test_treino_compartilhado_add_nao_authenticado_retorna_status_401(self,client):
        # Testando a  authenticacao metodo get
        resultado = client.get(self.url_retrieve(url=self.url))
        assert resultado.status_code == HTTP_401_UNAUTHORIZED

    def test_treino_compartilhado_add_authenticated_retorna_status_400(self,cliente_user):
        # Testando a authenticacao metodo post
        resultado = cliente_user.post(self.url_retrieve(url=self.url))
        assert resultado.status_code == HTTP_400_BAD_REQUEST

    def test_treino_compartilhadp_add_slug_campo_necessario(self,cliente_user):
        # Testando campo necessario para requisicao
        esperado = 'slug_compartilhado'
        resultado = cliente_user.post(self.url_retrieve(url=self.url))
        
        assert resultado.status_code == HTTP_400_BAD_REQUEST
        assert esperado in resultado.data
        assert len(resultado.data) == 1 

    def test_treino_compartilhado_add_slug_existe_retorna_status_201_sucesso(self,cliente_user,treino_compartilhado):
        # Testando a criacao com slug correto
        slug  = treino_compartilhado.slug
        dados = {'slug_compartilhado': slug}
        resultado = cliente_user.post(self.url_retrieve(url=self.url),data=dados)

        assert resultado.status_code == 201
        assert resultado.data == 'Sucesso'

    def test_treino_compartilhado_add_slug_nao_existe_error_404(self,cliente_user):
        # Testando error de slug inexistente
        dados = {'slug_compartilhado':'123'}
        resultado = cliente_user.post(self.url_retrieve(self.url),data=dados)

        assert resultado.status_code == HTTP_400_BAD_REQUEST
    
    def test_treino_compartilhado_add_slug_nao_existe_msg_error(self,cliente_user):
        # Tetando slug inexistente retorno de msg_error
        dados = {'slug_compartilhado':'123'}
        esperando_error = 'Objeto com slug=123 não existe.'
        resultado = cliente_user.post(self.url_retrieve(self.url),data=dados)
        resultado = resultado.data['slug_compartilhado']
        
        assert str(resultado[0]) == esperando_error
        assert resultado[0].code == 'does_not_exist' 

    def test_treino_comparilhado_add_criar_um_treino_videos(self,cliente_user,treino_compartilhado_com_videos):
        # Testando se a view esta criando corretamente o treino
        slug = treino_compartilhado_com_videos.slug
        dados = {'slug_compartilhado':slug}

        cliente_user.post(self.url_retrieve(self.url),data=dados)
        resultado =  models.TreinoVideosmodel.objects.filter(slug_compartilhado=slug)

        assert resultado.exists()

    def test_treino_compartilhado_add_criar_treino_vinculado_ao_usuario(self,treino_compartilhado_add_criado):
        # Testando se a view esta criando Treino vinculado ao usuario da requisicao
        _ , treino_compartilhado_com_videos = treino_compartilhado_add_criado
        treino = models.TreinoModel.objects.get(treino_nome=treino_compartilhado_com_videos.treino)
        assert treino.usuario.username == 'ClienteUser'

    def test_treino_compartilhado_add_criar_treino_videos_vinculado_ao_usuario(self,treino_compartilhado_e_treino_videos_criado_na_view_TreinoCompartilhadoAdd):
        # Testando se a view esta criando TreinoVideos vinculado ao usuario da requisicao
        treino_videos , _ = treino_compartilhado_e_treino_videos_criado_na_view_TreinoCompartilhadoAdd
        assert treino_videos.usuario.username == 'ClienteUser'

    def test_treino_compartilhado_add_criar_treino_videos_com_campos_do_compartilhado(self,treino_compartilhado_e_treino_videos_criado_na_view_TreinoCompartilhadoAdd):
        # Testando se view esta utilizando os campos da slug passada para criacao do TreinoVideos
        treino_videos , treino_compartilhado_com_videos = treino_compartilhado_e_treino_videos_criado_na_view_TreinoCompartilhadoAdd

        assert treino_videos.ordem == treino_compartilhado_com_videos.ordem
        assert treino_videos.slug_compartilhado == treino_compartilhado_com_videos.slug
        assert treino_videos.treino.treino_nome == treino_compartilhado_com_videos.treino

    def test_treino_compartilhado_add_com_treino_videos_ja_adicionado_msg_error_status_400(self,treino_compartilhado_add_criando_2):
        # Testando o retorno de msg_error quando a slug ja foi adicionando ao usuario
        esperado = 'Treino adicionado.'
        resposta_1 , resposta_2 = treino_compartilhado_add_criando_2

        assert resposta_2.data['slug_compartilhado'] == esperado
        assert resposta_2.status_code == HTTP_400_BAD_REQUEST
    
    def test_treino_compartilhado_add_qtd_treino_repetido_default(self):
        """
        -> Quantidado maxima de treino repetido criado.
        obs: houvendo mudança na quantidade de treino repetido atualizer este teste!
        """
        assert QTD_TREINO_REPETIDO == 5


    def test_treino_compartilhado_add_adiciona_ate_5_treino_com_mesmo_nome_quantidade_utrapassada_levanta_integrtyerror(self,cliente_user,treino_compartilhado_factory):
        # Testando quando criado 5 treino com mesmo nome levantar um error
        qtd_treino_repetido = 5
        quantidade_requisicao = 10
        with patch('apps.academia.views.QTD_TREINO_REPETIDO',new=qtd_treino_repetido):
            for i in range(0,quantidade_requisicao):
                treino_compartilhado = treino_compartilhado_factory.create(treino='Treino-repetido',slug=f'Treino-repetido-{i}')
                dados = {'slug_compartilhado': treino_compartilhado.slug }
                if i < qtd_treino_repetido:
                    resultado =cliente_user.post(self.url_retrieve(self.url),data=dados)
                    assert resultado.status_code == HTTP_201_CREATED
                else:
                    with raises(IntegrityError):
                        cliente_user.post(self.url_retrieve(self.url),data=dados)

        resultado = models.TreinoModel.objects.all()
        assert len(resultado) == qtd_treino_repetido
        
    @patch('apps.academia.views.QTD_TREINO_REPETIDO',5)
    def test_treino_compartilhado_add_adiciona_ate_5_treino_retorna_msg_error_limite_utrapassado(self,criando_5_model_treino_compartilhado_com_requisicao,cliente_user,treino_compartilhado_factory):
        # Testando a msg_error levatado a atigir o limite maximo permitido
        treino_compartilhado = treino_compartilhado_factory.create(treino='Treino-repetido',slug=f'Treino-repetido')
        dados = {'slug_compartilhado': treino_compartilhado.slug }
        
        with raises(IntegrityError) as resultado_msg_error:
            cliente_user.post(self.url_retrieve(self.url),data=dados)
        
        esperado_msg_error = "Limite atigido, favor apague treinos com nome que contem Treino-repetido."
        assert str(resultado_msg_error.value) == esperado_msg_error

    @patch('apps.academia.views.QTD_TREINO_REPETIDO',5)
    def test_treino_compartilhado_add_treinos_repetidos_criado_com_inicio_e_final_com_underline(self,criando_5_model_treino_compartilhado_com_requisicao):
        # Testand a criacao do treino repetido com '_ underline' para os treinos repetidos
        treinos = models.TreinoModel.objects.all()

        for i , treino in enumerate(treinos):
            assert treino.treino_nome.startswith(('_')*i)
            assert treino.treino_nome.endswith(('_')*i)
