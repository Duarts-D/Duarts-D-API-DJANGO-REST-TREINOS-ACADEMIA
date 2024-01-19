from rest_framework.test import APITestCase
from apps.academia.serializer import TreinoModelSerializer


class TreinoModelSeriliazerTest(APITestCase):
    def test_treinoModelserializer_campo_usuario_somente_para_leitura(self):
        dados = {'treino_nome':''}
        serializer = TreinoModelSerializer(data=dados)
        campo_leitura = serializer.fields['usuario'].read_only
        self.assertTrue(campo_leitura)