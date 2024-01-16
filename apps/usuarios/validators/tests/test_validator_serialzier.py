from apps.usuarios.validators.validator_serializer import senha_forte

def test_senha_forte_e_retornado_verdadeira():
    senha = 'UserTeste123'
    senha_2 = 'User123456'
    resultado = senha_forte(senha)
    resultado_2 = senha_forte(senha_2)

    assert resultado == True
    assert resultado_2 == True

def test_senha_forte_e_retornado_false():
    senha = '1234user'
    senha_2 = 'abc123456'
    resultado = senha_forte(senha)
    resultado_2 = senha_forte(senha_2)

    assert resultado == False
    assert resultado_2 == False