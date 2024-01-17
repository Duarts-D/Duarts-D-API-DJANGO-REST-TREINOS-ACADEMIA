from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class EquipamentoModel(models.Model):
    equipamento = models.CharField(max_length=255,verbose_name=_('Equipamento'))

    def __str__(self):
        return self.equipamento

    class Meta:
        verbose_name = _('Equipamento')
        verbose_name_plural = _('Equipamentos')

class GrupoMuscularModel(models.Model):
    grupo_muscular = models.CharField(max_length=255,verbose_name=_('Grupo Musucular'))

    def __str__(self):
        return self.grupo_muscular
    
    class Meta:
        verbose_name = _('Grupo Muscular')
        verbose_name_plural = _('Grupos Musculares')

class VideoModel(models.Model):
    video_nome = models.CharField(max_length=255,verbose_name=_('Exercicio'))
    video_id_youtube = models.CharField(max_length=255,verbose_name=_('Video id'))
    video_url = models.CharField(max_length=100,blank=True,null=True,verbose_name=_("video_url"))
    informacao = models.CharField(max_length=255,blank=True,null=True,verbose_name=_('Informacão'))
    imagem = models.ImageField(upload_to='img_videos/%Y/%m/%d',blank=True,null=True,verbose_name=_('Imagem'))
    video_id_didatico = models.CharField(max_length=50,blank=True,null=True,verbose_name=_('Video id didatico'))
    grupo_muscular = models.ForeignKey(GrupoMuscularModel,on_delete=models.SET_NULL,null=True,verbose_name=_('Grupo Muscular'))
    equipamento = models.ForeignKey(EquipamentoModel,on_delete=models.SET_NULL,null=True,verbose_name=_('Equipamento'))
    
    def save(self,*args,**kwargs):
        if len(self.video_id_youtube) > 2:
             self.video_url = 'https://www.youtube.com/embed/' + self.video_id_youtube
        saved = super().save(*args,**kwargs)
        return saved
    
    def __str__(self):
        return self.video_nome

    class Meta:
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')

class TreinoModel(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    treino_nome = models.CharField(max_length=40,verbose_name=_('Treino'))

    def __str__(self):
        return self.treino_nome 

    class Meta:
        verbose_name = _('Treino')
        verbose_name_plural = _('Treinos')

class TreinoVideosmodel(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    treino = models.ForeignKey(TreinoModel,on_delete=models.CASCADE)
    videos = models.ManyToManyField(VideoModel)
    ordem = models.CharField(max_length=200,default=None,null=True)

    def __str__(self):
        return self.treino.treino_nome
    
    class Meta:
        verbose_name = _('Treino Video')
        verbose_name_plural = _('Treinos Videos')