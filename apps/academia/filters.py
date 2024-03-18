from django_filters import rest_framework as filters
from .models import VideoModel


class VideosFilter(filters.FilterSet):
    videos = filters.CharFilter(field_name="video_nome", lookup_expr='icontains')
    grupos = filters.CharFilter(field_name='grupo_muscular__grupo_muscular',lookup_expr='icontains')
    equipamentos = filters.CharFilter(field_name='equipamento__equipamento',lookup_expr='icontains')

    class Meta:
        model = VideoModel
        fields = ['video_nome','grupo_muscular__grupo_muscular','equipamento__equipamento']
