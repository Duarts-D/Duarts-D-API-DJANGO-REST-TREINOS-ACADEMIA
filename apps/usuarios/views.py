from rest_framework import viewsets
from .serializer import UserCadastroSerializer
from django.contrib.auth.models import User

class CadastroViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserCadastroSerializer
    http_method_names = ['post']
