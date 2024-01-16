from django.urls import path,include
from rest_framework import routers
from .views import CadastroViewSet

router = routers.DefaultRouter()
router.register('cadastro',CadastroViewSet,basename='Cadastro')

urlpatterns = [
    path('',include(router.urls))
]

