from rest_framework import viewsets
from .serializer import UserCadastroSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

class CadastroViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserCadastroSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']
