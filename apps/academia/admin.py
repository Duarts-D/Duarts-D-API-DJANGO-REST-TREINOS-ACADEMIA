from django.contrib import admin
from .models import VideoModel,GrupoMuscularModel,EquipamentoModel


LIST_PAGE = 10

# Register your models here.
@admin.register(VideoModel)
class VideoAdmiModel(admin.ModelAdmin):
    list_display = ['video_nome','video_id_youtube','video_id_didatico']
    list_per_page = LIST_PAGE
    readonly_fields = ['video_url',]

@admin.register(EquipamentoModel)
class GrupoMuscularAdminModel(admin.ModelAdmin):
    list_display = ['id','equipamento',]
    list_per_page = LIST_PAGE

@admin.register(GrupoMuscularModel)
class EquipamentoModelAdmin(admin.ModelAdmin):
    list_display = ['id','grupo_muscular',]
    list_per_page = LIST_PAGE