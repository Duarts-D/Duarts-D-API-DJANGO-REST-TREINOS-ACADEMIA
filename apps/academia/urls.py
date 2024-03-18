from django.urls import path
from apps.academia import views

urlpatterns = [
    path('c-criar/', views.TreinoCompartilhadoViewCreate.as_view(),name='compartilhar-criar'),
    path('c-retrieve/<slug:slug>/',views.TreinoCompartilhadoRetrieve.as_view(),name='compartilhar-retrieve'),
    path('c-add/',views.TreinoCompartilhadoAddViewCreate.as_view(),name='compartilhar-add'),
    path('videos/',views.VideosViewList.as_view(),name='videos-list'),
]