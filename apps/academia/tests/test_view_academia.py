from rest_framework.test import APITestCase
from rest_framework.status import (HTTP_405_METHOD_NOT_ALLOWED,HTTP_400_BAD_REQUEST,
                                   HTTP_201_CREATED,HTTP_200_OK,HTTP_204_NO_CONTENT,
                                   HTTP_404_NOT_FOUND)
from apps.academia.tests.test_geradores_base import Geradores_base_mixin
from django.urls import reverse
from django.contrib.auth.models import User
from apps.academia.models import TreinoModel

class TreinoModelViewSetTest(Geradores_base_mixin,APITestCase):
    def setUp(self):
        self.username = 'UserTest123'
        self.password = 'Pasword1234'
        self.cadastro = self.cadastro_usuario(username=self.username,password=self.password)
        self.url = reverse('treino-listas-list')
        self.client.login(username=self.username, password=self.password)
        TreinoModel.objects.create(usuario=self.cadastro,treino_nome='Treino lista 1')
        TreinoModel.objects.create(usuario=self.cadastro,treino_nome='Treino lista 2')


    def test_treinomodelviewset_get_retorna_codigo_200(self):
        resposta = self.client.get(self.url)
        self.assertEqual(resposta.status_code,HTTP_200_OK)

    def test_treinomodelviewset_post_retorna_codigo_200(self):
        reposta = self.client.get(self.url)
        self.assertEqual(reposta.status_code,HTTP_200_OK)

    def test_treinomodelviewset_put_retorna_codigo_404(self):
        resposta = self.client.put(f'{self.url}1/')
        self.assertEqual(resposta.status_code,HTTP_405_METHOD_NOT_ALLOWED)


    def test_treinomodelviewset_patch_retorna_codigo_200(self):
        resposta = self.client.patch(f'{self.url}1/')
        self.assertEqual(resposta.status_code , HTTP_200_OK)

    def test_treinomodelviewset_delete_retorna_204(self):
        resposta = self.client.delete(self.url+'1/')
        self.assertEqual(resposta.status_code,HTTP_204_NO_CONTENT)

    def test_treinomodelviewset_get_retorna_query_somente_do_usuario(self):
        usuario_1 = self.username
        usuario_2 = self.cadastro_usuario(username="Usuario2",password='Password123')
        TreinoModel.objects.create(usuario=usuario_2,treino_nome="Usuario_2 treino 1")
        TreinoModel.objects.create(usuario=usuario_2,treino_nome="Usuario_2 treino 2")
        TreinoModel.objects.create(usuario=usuario_2,treino_nome="Usuario_2 treino 3")

        resposta = self.client.get(self.url)
        resposta = resposta.data
        self.assertEqual(len(resposta), 2)
        self.assertEqual(resposta[0]['usuario'],usuario_1)
        self.assertEqual(resposta[0]['treino_nome'],'Treino lista 1')
        self.assertEqual(resposta[1]['usuario'],usuario_1)
        self.assertEqual(resposta[1]['treino_nome'],'Treino lista 2')
        self.client.logout()

        self.client.login(username="Usuario2",password="Password123")
        resposta_2 = self.client.get(self.url)
        resposta_2 = resposta_2.data 

        self.assertEqual(len(resposta_2), 3)
        self.assertEqual(resposta_2[0]['usuario'],usuario_2.username)
        self.assertEqual(resposta_2[0]['treino_nome'],'Usuario_2 treino 1')
        self.assertEqual(resposta_2[1]['usuario'],usuario_2.username)
        self.assertEqual(resposta_2[1]['treino_nome'],'Usuario_2 treino 2')
        self.assertEqual(resposta_2[2]['usuario'],usuario_2.username)
        self.assertEqual(resposta_2[2]['treino_nome'],'Usuario_2 treino 3')

    def test_treinomodelviewset_post_retornar_query_vinculado_ao_usuario_e_id_e_nome_do_treino_codigo_200(self):
        dados = {
            "treino_nome":"Teste post"
        }        
        resposta = self.client.post(self.url, data=dados)
        esperado = {'id': 3, 'treino_nome': 'Teste post', 'usuario': 'UserTest123'}
        self.assertEqual(resposta.data,esperado)
        self.assertEqual(len(resposta.data),3)
        self.assertEqual(resposta.status_code,HTTP_201_CREATED)

    def test_treinomodeviewset_patch_retorna_query_vinculado_ao_usuario_e_id_e_nome_do_treino_codigo_200(self):
        nome_treino = 'Teste patch'
        dados = {
            "treino_nome":nome_treino
        }
        resposta = self.client.patch(self.url+'1/',data=dados)
        esperado = {'id': 1, 'treino_nome': nome_treino, 'usuario': 'UserTest123'}
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