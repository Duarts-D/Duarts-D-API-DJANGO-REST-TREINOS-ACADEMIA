from rest_framework.test import APITestCase
from django.urls import reverse,resolve
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED,HTTP_400_BAD_REQUEST,HTTP_201_CREATED
from test_cadastro_base import CadastroMixin


class CadastroViewsetTest(CadastroMixin,APITestCase):
    def setUp(self):
        self.url_cadastro = reverse('Cadastro-list')

    def test_cadastroviewset_methodo_get_retorna_codigo_405(self):
        resposta = self.client.get(self.url_cadastro)
        self.assertEqual(resposta.status_code,HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_cadastroviewset_methodo_post_retorna_codigo_400(self):
        resposta = self.client.post(self.url_cadastro)
        self.assertEqual(resposta.status_code,HTTP_400_BAD_REQUEST)

    def test_cadastroviewset_methodo_put_retorna_codigo_405(self):
        resposta = self.client.put(self.url_cadastro,data={})
        self.assertEqual(resposta.status_code,HTTP_405_METHOD_NOT_ALLOWED)

    def test_cadastroviewset_methodo_patch_retorna_codigo_405(self):
        resposta = self.client.patch(self.url_cadastro,data={})
        self.assertEqual(resposta.status_code,HTTP_405_METHOD_NOT_ALLOWED)

    def test_cadastroviewset_methodo_delete_retorna_codigo_405(self):
        resposta = self.client.delete(self.url_cadastro,data={})
        self.assertEqual(resposta.status_code,HTTP_405_METHOD_NOT_ALLOWED)

    
    def test_cadastroviewset_methodo_options_retorna_codigo_405(self):
        resposta = self.client.options(self.url_cadastro)
        self.assertEqual(resposta.status_code,HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_cadastroviewset_methodo_head_retorna_codigo_405(self):
        resposta = self.client.head(self.url_cadastro)
        self.assertEqual(resposta.status_code,HTTP_405_METHOD_NOT_ALLOWED)


    def test_cadastroviewset_methodo_post_retorna_codigo_201(self):
        dados = self.dados_usuario()
        resposta = self.client.post(self.url_cadastro,data=dados)
        self.assertEqual(resposta.status_code,HTTP_201_CREATED)

    def test_cadastroviewset_methodo_post_retorna_errors_de_cadastros_username_e_email_iguais_retorno_codigo_400(self):
        self.cadastro_usuario()
        dados = self.dados_usuario()
        resposta = self.client.post(self.url_cadastro,data=dados)
        erros = resposta.data

        erros_username = erros['username'][0]
        self.assertEqual(erros_username.title(),'Um Usuário Com Este Nome De Usuário Já Existe.')
        self.assertEqual(erros_username.code,'invalid')

        erros_email = erros['email'][0]
        self.assertEqual(erros_email.title(),'Este Email Ja Foi Utilizado')
        self.assertEqual(erros_email.code,'invalid')


        self.assertEqual(resposta.status_code,HTTP_400_BAD_REQUEST)

    def test_cadastroviewset_methodo_post_nao_aceita_itens_em_branco_o_retorno_e_este_campo_e_obrigatorio_para_os_campo_ajustado(self):
        """Garante que os campo utilizado no post sao os unicos essenciais"""
        
        resposta = self.client.post(self.url_cadastro,data={})
        
        self.assertEqual(resposta.status_code,HTTP_400_BAD_REQUEST)
        campos = {
            'username':['Este campo é obrigatório.'],
            'first_name':['Este campo é obrigatório.'],
            'last_name':['Este campo é obrigatório.'],
            'email':['Este campo é obrigatório.'],
            'password':['Este campo é obrigatório.'],
            'repeat_password':['Este campo é obrigatório.']
        }
        self.assertEqual(resposta.data,campos)
    
    def test_cadastroviewset_methodo_post_senha_formato_incorreto_retorna_error_400_e_msg_explicativa(self):
        dados = self.dados_usuario()
        dados.update({'password':'user123456',
                      'repeat_password':'user123456'})
        resposta = self.client.post(self.url_cadastro,data=dados)
        error = resposta.data['password'][0].title()
        msg ='A Senha Deve Ter Pelo Menos Uma Letra Maiúscula, Uma Letra Minúscula E Um Número. O Comprimento Deve Ser Pelo Menos 8 Caracteres.'
        self.assertEqual(resposta.status_code,HTTP_400_BAD_REQUEST)
        self.assertEqual(error,msg)

    def test_cadastroviewset_methodo_post_senha_formato_correto_retorna_codigo_201_e_campos_retornado_username_first_name_last_name_email(self):
        dados = self.dados_usuario()
        resposta = self.client.post(self.url_cadastro,data=dados)
        retorno = resposta.data
        campos = [{'username': 'TestUser', 'first_name': 'User', 'last_name': 'Teste', 'email': 'user@email.com'}]
        self.assertEqual(resposta.status_code,HTTP_201_CREATED)
        self.assertIn(retorno,campos)