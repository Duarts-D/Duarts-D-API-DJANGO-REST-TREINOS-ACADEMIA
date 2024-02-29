from django.urls import path
from .views import TreinoCompartilhadoCreate,TreinoCompartilhadoRetrieve
urlpatterns = [
    path('c-criar/',TreinoCompartilhadoCreate.as_view(),name='compartilhar-criar'),
    path('c-retrieve/<slug:slug>/',TreinoCompartilhadoRetrieve.as_view(),name='compartilhar-retrieve'),
]

