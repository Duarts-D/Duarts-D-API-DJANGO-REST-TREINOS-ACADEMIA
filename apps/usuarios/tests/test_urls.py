from rest_framework.test import APITestCase
from django.urls import reverse

class CadastroUrlsTeste(APITestCase):
    def test_cadastroviewset_url_esta_correto(self):
        url = reverse('Cadastro-list')
        self.assertEqual(url,'/cadastro/')