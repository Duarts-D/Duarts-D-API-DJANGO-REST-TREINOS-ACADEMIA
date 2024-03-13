from django.contrib import admin
from .models import (VideoModel,GrupoMuscularModel,EquipamentoModel,
                    TreinoModel, TreinoVideosmodel,TreinosCompartilhadosModel)



LIST_PAGE = 10

# Register your models here.
@admin.register(VideoModel)
class VideoAdmiModel(admin.ModelAdmin):
    list_display = ['id','video_nome','video_id_youtube','video_id_didatico']
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

@admin.register(TreinoModel)
class TreinoModelAdmin(admin.ModelAdmin):
    list_display = ['id','treino_nome','usuario']
    list_per_page = LIST_PAGE

@admin.register(TreinoVideosmodel)
class TreinoVideoModelAdmin(admin.ModelAdmin):
    list_display = ['id','usuario','treino']
    list_per_page = LIST_PAGE

@admin.register(TreinosCompartilhadosModel)
class TreinoCompartilhadoAdmin(admin.ModelAdmin):
    list_display = ['id','treino','slug']
    list_per_page = LIST_PAGE
    list_filter =(('videos__publicado',admin.BooleanFieldListFilter),)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "videos":
            kwargs["queryset"] = VideoModel.objects.filter(publicado=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs) 