from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


TAMANHO_LENGTH_MIN = 4

def validade_str_minimo_length(value):
    if len(str(value)) < TAMANHO_LENGTH_MIN:
        raise ValidationError(
            _('Deve conter pelo menos 4 caracteristicos!'),
            params={'value':value},
            )