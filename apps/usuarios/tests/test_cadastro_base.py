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
    
    def cadastro_usuario(self):
        dados = self.dados_usuario()
        dados.pop('repeat_password')
        User.objects.create(**dados)
