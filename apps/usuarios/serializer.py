from django.contrib.auth.models import User
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from collections import defaultdict
from apps.usuarios.validators.validator_serializer import senha_forte


class UserCadastroSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=2,max_length=50,required=True)
    repeat_password = serializers.CharField(
        max_length=50,min_length=8,
        label=_('Repetir Senha'),
        write_only=True)
    first_name = serializers.CharField(min_length=2,max_length=100,required=True)
    last_name = serializers.CharField(min_length=2,max_length=100,required=True)
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','repeat_password',]
        extra_kwargs = {
            'password': {'write_only': True },
        }       
        
    def validate(self, data):
        _my_errors = defaultdict(list)
        email = data['email']
        email_existe = User.objects.filter(email=email).exists()

        senha = data['password']
        senha_2 = data['repeat_password']

        usuario = data['username']
        usuario_existe = User.objects.filter(username=usuario).exists()


        if usuario_existe:
            _my_errors['username'].append(_('Um usuário com este nome de usuário já existe.'))
        if email_existe:
            _my_errors['email'].append(_('Este email ja foi utilizado'))
        
        if not senha_forte(senha):
            _my_errors['password'].append(_('A senha deve ter pelo menos uma letra maiúscula, '
                                            'uma letra minúscula e um número. O comprimento deve ser '
                                            'pelo menos 8 caracteres.'))

        if senha != senha_2:
            _my_errors['password'].append(_('As senhas não coincidem'))
            _my_errors['repeat_password'].append(_('As senhas não coincidem'))
        
        if _my_errors:
            raise serializers.ValidationError(_my_errors)
        return data
    
    def create(self, validated_data):
        validated_data.pop('repeat_password')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user