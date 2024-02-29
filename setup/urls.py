"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from apps.usuarios import views as view_usuario
from apps.academia import views as view_academia


router = routers.DefaultRouter()
router.register('cadastro',view_usuario.CadastroViewSet,basename='Cadastro')
router.register('treinos',view_academia.TreinoCRUDViewset,basename='treino-listas')
router.register('videos-treinos-lista',view_academia.TreinoVideoslistaViewSet,basename='treino-videos-listas')
router.register('videos-treinos',view_academia.TreinoVideosCUDViewSet,basename='treino-videos')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('',include('apps.academia.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

