from apps.academia.utils import criar_slug

class TestUtils:
    def test_criar_slug_retorna_sequencia_de_40_caracteriscos_mais_parametro_passado(self):
        nome = 'dado'
        resultado  = criar_slug(nome)
        # Resposta
        resultado = len(resultado)
        assert resultado == (len(nome)+40)
    
    def test_criar_slug_contem_a_palavra_passada_por_paramentro_dados(self):
        nome = 'dados'
        resultado = criar_slug(nome)
        assert  (nome in resultado) == True