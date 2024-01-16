from rest_framework.test import APITestCase
from apps.usuarios.serializer import UserCadastroSerializer
from parameterized import parameterized
from django.contrib.auth.models import User

class UserCadastroSerializerTest(APITestCase):
    def setUp(self):
        self.dados = {
            'username':'TestUser',
            'first_name':'User',
            'last_name':'Teste',
            'email':'user@email.com',
            'password':'userTest123',
            'repeat_password':'userTest123'
        }
    
    def serializador(self,dados):
        serializador = UserCadastroSerializer(data=dados)
        serializador.is_valid()
        return serializador
    
    @staticmethod
    def campos_do_serializer():
        campos = [
            ('username'),
            ('first_name'),
            ('last_name'),
            ('email'),
            ('password'),
            ('repeat_password'),
            ]
        return campos
    
    def cadastro_usuario(self):
        dados = self.dados.copy()
        dados.pop('repeat_password')
        User.objects.create(**dados)

    def test_serializer_validacoes_e_verdadeira(self):
        dados = self.dados
        serializer = self.serializador(dados)
        self.assertEqual(serializer.is_valid(), True)

    @parameterized.expand(campos_do_serializer())
    def test_serializer_validacoes_e_falso(self,campo):
        dados = self.dados
        dados.update({campo :''})
        serializer = self.serializador(dados)
        self.assertEqual(serializer.is_valid(),False)

    def test_serializer_campos_necessarios_sao_username_first_name_last_name_email_password_repeat_password(self):
        dados = self.dados
        campos_necessario = {'repeat_password', 'email', 'first_name', 'username', 'last_name', 'password'}
        serializer = self.serializador(dados)
        serializer_campos = set(serializer.fields.keys())
        serializer_qtd_campos = len(serializer_campos)
        self.assertEqual(serializer_campos,campos_necessario)
        self.assertEqual(serializer_qtd_campos,6)

    def test_serializer_campos_password_e_repeat_password_estao_em_modo_write_only_igual_a_verdadeiro(self):
        dados = self.dados
        serializer = self.serializador(dados)
        self.assertEqual(serializer.get_extra_kwargs()['password']['write_only'],True)

    @parameterized.expand(campos_do_serializer())
    def test_serializer_todos_os_campos_requeridos_igual_true_e_nao_pode_ficar_em_branco(self,campo):
        serializer = self.serializador({})
        erros_required = serializer.errors
        erros = erros_required[campo][0]
        self.assertEqual(erros.code,"required",)
        self.assertEqual(erros.title(),'Este Campo É Obrigatório.')

        dados = self.dados
        dados.update({campo:''})
        serializer_blank = self.serializador(dados)
        erros_blak = serializer_blank.errors
        erros = erros_blak[campo][0]
        self.assertEqual(erros.code,'blank')
        self.assertEqual(erros.title(),'Este Campo Não Pode Ser Em Branco.')
    
    def test_serializer_messages_erros_personalizada_para_os_campo_email(self):
        self.cadastro_usuario()
        dados = self.dados
        serializer = self.serializador(dados)
        error_msg = serializer.errors
        error = error_msg['email'][0]
        self.assertEqual(error.title(),'Este Email Ja Foi Utilizado')
        self.assertEqual(error.code,'invalid')

    def test_serializer_messages_erros_personalizada_para_os_campo_username(self):
        self.cadastro_usuario()
        dados = self.dados
        serializer = self.serializador(dados)
        error_msg = serializer.errors
        error = error_msg['username'][0]
        self.assertEqual(error.title(),'Um Usuário Com Este Nome De Usuário Já Existe.')
        self.assertEqual(error.code,'invalid')



    def test_serializer_messages_erros_personalizada_para_os_campo_password_e_repeat_password_sao_diferentes(self):
        self.cadastro_usuario()
        dados = self.dados
        dados.update({'password':'user12345678'})
        serializer = self.serializador(dados)
        error_msg = serializer.errors
        
        error_password = error_msg['password'][0]
        self.assertEqual(error_password.title(),'As Senhas Não Coincidem')
        self.assertEqual(error_password.code,'invalid')
        
        error_repeat_password = error_msg['repeat_password'][0]
        self.assertEqual(error_repeat_password.title(),'As Senhas Não Coincidem')
        self.assertEqual(error_repeat_password.code,'invalid')

    def test_serializer_create_esta_salvando_corretamente_password_hashed(self):
        dados = self.dados
        senha = 'TesTeUser123'
        dados.update({
            'password': senha,
            'repeat_password':senha
            })
        serializer = self.serializador(dados)
        serializer.create(serializer.validated_data)
        usuario_cadastrado = User.objects.get(id=1)
        self.assertTrue(usuario_cadastrado.check_password(senha))