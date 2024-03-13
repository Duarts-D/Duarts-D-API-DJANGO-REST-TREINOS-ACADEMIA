from rest_framework.test import APITestCase
from django.urls import reverse
from pytest import raises
from django.urls.exceptions import NoReverseMatch

class AcademiaUrlsTeste(APITestCase):
    def test_treino_viewset_url(self):
        url = reverse('treino-listas-list')
        self.assertEqual(url,'/treinos/')

    def test_treinocompartilhado_create_url(self):
        url = reverse('compartilhar-criar')
        self.assertEqual(url,'/c-criar/')


    def test_treinocompartilhado_retrieve_url_slug_obrigatorio(self):
        # A url deve funcionar somente pra retrieve com pk como argumento.
        with raises(NoReverseMatch):
            reverse('compartilhar-retrieve')

    def test_treinocompartilhado_retrieve_url(self):
        url = reverse('compartilhar-retrieve',kwargs={'slug':1})
        self.assertEqual(url,'/c-retrieve/1/')

    def test_treinocomapartilhado_add_url(self):
        url = reverse('compartilhar-add')
        self.assertEqual(url, '/c-add/')