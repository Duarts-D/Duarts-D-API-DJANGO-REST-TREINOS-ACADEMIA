from rest_framework.test import APITestCase
from rest_framework.status import (HTTP_405_METHOD_NOT_ALLOWED,HTTP_400_BAD_REQUEST,
                                   HTTP_201_CREATED,HTTP_200_OK,HTTP_204_NO_CONTENT,
                                   HTTP_404_NOT_FOUND)
from apps.academia.tests._utils_geradores_base import GeradoresBaseMixin
from django.urls import reverse
from apps.academia.models import TreinoModel



class TreinoCRUDViewSetTest(GeradoresBaseMixin,APITestCase):
    def setUp(self):
        self.username , self.usuario = self.criar_usuario_logout_logar()
        self.url = reverse('treino-listas-list')
        self.nomes_treino_usuario = self.criar_treinos_multiplicos(2,self.usuario)


    def test_treinocrud_viewset_get_retorna_codigo_200(self):
        resposta = self.client.get(self.url)
        self.assertEqual(resposta.status_code,HTTP_200_OK)

    def test_treinocrud_viewset_post_retorna_codigo_201(self):
        reposta = self.client.post(self.url,data={'treino_nome':'videos'})
        self.assertEqual(reposta.status_code,HTTP_201_CREATED)

    def test_treinocrud_viewset_put_retorna_codigo_404(self):
        resposta = self.client.put(f'{self.url}1/')
        self.assertEqual(resposta.status_code,HTTP_405_METHOD_NOT_ALLOWED)


    def test_treinocrud_viewset_patch_retorna_codigo_200(self):
        resposta = self.client.patch(f'{self.url}1/',data={'treino_nome':'treino'})
        self.assertEqual(resposta.status_code , HTTP_200_OK)

    def test_treinocrud_viewset_patch_treino_nome_obrigatorio_status_400(self):
        resposta = self.client.patch(f'{self.url}1/')
        self.assertEqual(resposta.status_code,HTTP_400_BAD_REQUEST)
        resposta_error = resposta.data['treino_nome']
        esperado_error =  'Este campo é obrigatório.'
        self.assertEqual(str(resposta_error),esperado_error)
        self.assertEqual(resposta_error.code,'invalid')

    

    def test_treinocrud_viewset_delete_retorna_204(self):
        resposta = self.client.delete(self.url+'1/')
        self.assertEqual(resposta.status_code,HTTP_204_NO_CONTENT)

    def test_treinocrud_viewset_get_retorna_query_somente_do_usuario(self):
        # Usuarios
        usuario_1 = self.username
        usuario_2_username = "Usuario2"
        usuario_2_password = 'Password123'
        usuario_2 = self.cadastro_usuario(username=usuario_2_username,password=usuario_2_password)

        # Treinos
        nomes_treinos_usuario_1 = self.nomes_treino_usuario
        nomes_treinos_usuario_2 = self.criar_treinos_multiplicos(3,usuario_2)

        # CLiente 1
        resposta = self.client.get(self.url)
        resposta = resposta.data
        self.assertEqual(len(resposta), 2)
        self.assertEqual(resposta[0]['usuario'],usuario_1)
        self.assertEqual(resposta[0]['treino_nome'],nomes_treinos_usuario_1[0].treino_nome)
        self.assertEqual(resposta[1]['usuario'],usuario_1)
        self.assertEqual(resposta[1]['treino_nome'],nomes_treinos_usuario_1[1].treino_nome)

        # Cliente 2
        self.criar_usuario_logout_logar(username=usuario_2_username,password=usuario_2_password)
        resposta_2 = self.client.get(self.url)
        resposta_2 = resposta_2.data 

        self.assertEqual(len(resposta_2), 3)
        self.assertEqual(resposta_2[0]['usuario'],usuario_2.username)
        self.assertEqual(resposta_2[0]['treino_nome'],nomes_treinos_usuario_2[0].treino_nome)
        self.assertEqual(resposta_2[1]['usuario'],usuario_2.username)
        self.assertEqual(resposta_2[1]['treino_nome'],nomes_treinos_usuario_2[1].treino_nome)
        self.assertEqual(resposta_2[2]['usuario'],usuario_2.username)
        self.assertEqual(resposta_2[2]['treino_nome'],nomes_treinos_usuario_2[2].treino_nome)

    def test_treinocrud_viewset_post_retornar_query_vinculado_ao_usuario_e_id_e_nome_do_treino_codigo_200(self):
        dados = {
            "treino_nome":"Teste post"
        }        
        resposta = self.client.post(self.url, data=dados)
        esperado = {'id': 3, 'treino_nome': 'Teste post', 'usuario': self.username}
        self.assertEqual(resposta.data,esperado)
        self.assertEqual(len(resposta.data),3)
        self.assertEqual(resposta.status_code,HTTP_201_CREATED)

    def test_treinomodeviewset_patch_retorna_query_vinculado_ao_usuario_e_id_e_nome_do_treino_codigo_200(self):
        nome_treino = 'Teste patch'
        dados = {
            "treino_nome":nome_treino
        }
        resposta = self.client.patch(self.url+'1/',data=dados)
        esperado = {'id': 1, 'treino_nome': nome_treino, 'usuario': self.username}
        self.assertEqual(resposta.status_code,HTTP_200_OK)
        self.assertEqual(resposta.data,esperado)
    
    def test_treinomodeviewset_patch_retorna_404_quando_query_nao_e_vinculado_ao_usuario_codigo_404(self):
        self.criar_treino()
        resposta = self.client.patch(self.url+'3/')
        item = TreinoModel.objects.get(id=3)
        self.assertEqual(resposta.status_code,HTTP_404_NOT_FOUND)
        self.assertNotEqual(item.usuario,self.username)        

    def test_treinomodeviewset_delete_retorna_204_quando_a_query_e_do_vinculado_ao_usuario(self):
        resposta = self.client.delete(self.url+'2/')
        self.assertEqual(resposta.status_code, HTTP_204_NO_CONTENT)
    
    def test_treinomodeviewset_delete_retorna_404_quando_a_query_nao_e_do_usuario(self):
        self.criar_treino()
        resposta = self.client.delete(self.url+'3/')
        self.assertEqual(resposta.status_code,HTTP_404_NOT_FOUND)

    def test_treinomodeviewset_patch_error_nome_treino_ja_criado(self):
        treino = 'treinos_x'
        resposta = self.client.post(self.url,data={'treino_nome':treino})
        self.assertEqual(resposta.status_code,HTTP_201_CREATED)

        # Resposta criacao repetida
        resposta_2 = self.client.post(self.url,data={'treino_nome':treino})
        self.assertEqual(resposta_2.status_code, HTTP_400_BAD_REQUEST)
        resposta_2_error = resposta_2.data['treino_nome']
        esperado_error = f'Treino existente {treino}.'
        self.assertEqual(str(resposta_2_error), esperado_error)
        self.assertEqual(resposta_2_error.code, 'invalid')
