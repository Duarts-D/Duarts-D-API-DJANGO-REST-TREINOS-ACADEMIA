import random
import string

def criar_slug(nome_treino:str):
    """
    -> Criar um slug para compartilhamento com nome do treino. 
    :retun: slug
    """
    caracteristicos = string.ascii_letters + string.digits
    slug = ''.join(random.choice(caracteristicos) for _ in range(40))
    a = random.randint(0,40)
    slug_treino = slug[:a] + str(nome_treino) + slug[a:] 
    return slug_treino