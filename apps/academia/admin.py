from django.contrib import admin
from .models import VideoModel

# Register your models here.
@admin.register(VideoModel)
class VideoAdmiModel(admin.ModelAdmin):
    list_display = ['video_nome','video_id_youtube','video_id_didatico']
    list_per_page = 10