from django.db import models
from django.utils.translation import gettext_lazy as _


class VideoModel(models.Model):
    video_nome = models.CharField(max_length=255,verbose_name=_('Exercicio'))
    video_id_youtube = models.CharField(max_length=255,verbose_name=_('Video id'))
    video_url = models.CharField(max_length=100,blank=True,null=True,verbose_name=_("video_url"))
    informacao = models.CharField(max_length=255,blank=True,null=True,verbose_name=_('Informacão'))
    imagem = models.ImageField(upload_to='img/',blank=True,null=True,verbose_name=_('Imagem'))
    video_id_didatico = models.CharField(max_length=50,blank=True,null=True,verbose_name=_('Video id didatico'))
    def save(self,*args):
        if len(self.video_id_youtube) > 2:
            self.video_url = 'https://www.youtube.com/embed/' + self.video_id_youtube
        return super().save(*args)

    def __str__(self):
        return self.video_nome
    