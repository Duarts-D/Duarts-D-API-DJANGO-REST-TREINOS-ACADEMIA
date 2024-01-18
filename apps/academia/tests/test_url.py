from rest_framework.test import APITestCase
from django.urls import reverse

class TreinoUrlsTeste(APITestCase):
    def test_treinoviewset_url_esta_correto(self):
        url = reverse('treino-listas-list')
        self.assertEqual(url,'/treinos/')