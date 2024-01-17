from django.contrib.auth.models import User

class CadastroMixin:
    def dados_usuario(self):
        dados = {
            'username':'TestUser',
            'first_name':'User',
            'last_name':'Teste',
            'email':'user@email.com',
            'password':'userTest123',
            'repeat_password':'userTest123'
        }
        return dados
    
    def cadastro_usuario(self,username='TestUser'):
        dados = self.dados_usuario()
        dados['username'] = username
        dados.pop('repeat_password')
        user = User.objects.create(**dados)
        return user