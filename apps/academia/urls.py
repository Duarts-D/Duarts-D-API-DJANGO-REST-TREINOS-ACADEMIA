from django.urls import path
from apps.academia import views

urlpatterns = [
    path('c-criar/', views.TreinoCompartilhadoCreate.as_view(),name='compartilhar-criar'),
    path('c-retrieve/<slug:slug>/',views.TreinoCompartilhadoRetrieve.as_view(),name='compartilhar-retrieve'),
    path('c-add/',views.TreinoCompartilhadoAdd.as_view(),name='compartilhar-add'),
]

