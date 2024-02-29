from apps.academia.validators.validator import validade_str_minimo_length
from pytest import raises
from django.core.exceptions import ValidationError

def test_validade_minimo_quantidade_incorreta_retornar_error():
    nome = 'tes'
    # Resposta
    with raises(ValidationError) as error:
        validade_str_minimo_length(value=nome)
    
    erro_msg_esperado = "['Deve conter pelo menos 4 caracteristicos!']"
    assert str(error.value) == erro_msg_esperado