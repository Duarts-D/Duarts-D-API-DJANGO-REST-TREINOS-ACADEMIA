from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.urls import reverse
from apps.academia.validators.validator import validade_str_minimo_length

class VideoManage(models.Manager):
    def get_publicado(self):
        return self.filter(
            publicado=True
        )

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
    objects = VideoManage()
    video_nome = models.CharField(max_length=255,verbose_name=_('Exercicio'))
    video_id_youtube = models.CharField(max_length=255,verbose_name=_('Video id'))
    video_url = models.CharField(max_length=100,blank=True,null=True,verbose_name=_("video_url"))
    informacao = models.CharField(max_length=255,blank=True,null=True,verbose_name=_('Informacão'))
    imagem = models.ImageField(upload_to='img_videos/%Y/%m/%d',blank=True,null=True,verbose_name=_('Imagem'))
    video_id_didatico = models.CharField(max_length=50,blank=True,null=True,verbose_name=_('Video id didatico'))
    grupo_muscular = models.ForeignKey(GrupoMuscularModel,on_delete=models.SET_NULL,null=True,verbose_name=_('Grupo Muscular'))
    equipamento = models.ForeignKey(EquipamentoModel,on_delete=models.SET_NULL,null=True,verbose_name=_('Equipamento'))
    publicado = models.BooleanField(default=False,verbose_name=_('Publicado'))
    
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
        return str(self.treino_nome)

    class Meta:
        verbose_name = _('Treino')
        verbose_name_plural = _('Treinos')
        unique_together = ['usuario','treino_nome']


class TreinoVideosmodel(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    treino = models.ForeignKey(TreinoModel,on_delete=models.CASCADE)
    videos = models.ManyToManyField(VideoModel)
    ordem = models.CharField(max_length=200,default=None,null=True,blank=True)
    slug_compartilhado = models.SlugField(max_length=200,blank=True)

    def __str__(self):
        return str(self.treino)
    
    class Meta:
        verbose_name = _('Treino Video')
        verbose_name_plural = _('Treinos Videos')
        unique_together = ['usuario','treino']


class TreinosCompartilhadosModel(models.Model):
    treino = models.CharField(max_length=40,verbose_name=_('Treino'),blank=False,validators=[validade_str_minimo_length])
    videos = models.ManyToManyField(VideoModel)
    ordem = models.CharField(max_length=200,default=None,null=True,blank=True)
    slug = models.SlugField(unique=True,blank=True,max_length=200)

    class Meta:
        verbose_name = _('Treino Compartilhado')
        verbose_name_plural = _('Treinos compartilhados')
    