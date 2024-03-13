from rest_framework import serializers
from apps.academia.models import TreinoModel,TreinoVideosmodel,VideoModel,TreinosCompartilhadosModel
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError

class TreinoModelSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = TreinoModel
        fields = ['id','treino_nome','usuario']

    def create(self,validated_data):
        validated_data['usuario'] = self.context['request'].user
        validate = super().create(validated_data)
        return validate
    
    def to_internal_value(self, data):
        ret  = super().to_internal_value(data)
        user = self.context['request'].user
        treino = ret.get('treino_nome',None)
        treino_exist = TreinoModel.objects.filter(usuario=user,treino_nome=treino).exists()
        if treino_exist:
           raise ValidationError({'treino_nome':_(f'Treino existente {treino}.')})
        if treino == None:
            raise ValidationError({'treino_nome':_("Este campo é obrigatório.")})
        return ret


class VideosSerializer(serializers.ModelSerializer):
    grupo_muscular = serializers.StringRelatedField()
    equipamento = serializers.StringRelatedField()
    id_video = serializers.SerializerMethodField(method_name='get_id_video')

    class Meta:
        model = VideoModel
        fields = [
            'id_video','video_nome','video_id_youtube','video_url',
            'informacao','imagem','video_id_didatico',
            'grupo_muscular','equipamento'
            ]

    def get_id_video(self,objeto):
        return objeto.id


class TreinoVideosSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(read_only=True)
    videos = VideosSerializer(many=True,read_only=True)
    treino = serializers.StringRelatedField(read_only=True)
    treino_id = serializers.PrimaryKeyRelatedField(source='treino',read_only=True)

    class Meta:
        model = TreinoVideosmodel
        fields = ['id','usuario','treino','treino_id','videos','ordem']


class TreinoVideosSerializerPost(serializers.ModelSerializer):
    videos = serializers.PrimaryKeyRelatedField(queryset=VideoModel.objects.get_publicado(),required=False,many=True)
    class Meta:
        model = TreinoVideosmodel
        fields = ['id','treino','videos','ordem']
    
    def validate_treino(self,value):
        user = self.context['request'].user
        if user.pk != value.usuario.pk:
            raise ValidationError(_(f'Pk inválido "{value.pk}" - objeto não existe.'))
        return value
    
class TreinoCompartilhadoSerializerCreate(serializers.Serializer):
    treino = serializers.PrimaryKeyRelatedField(queryset=TreinoVideosmodel.objects.all())#read_only=True
    class Meta:
        fields = ['treino',]

    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        treino_model = value['treino']
        user = self.context['request'].user
        if not treino_model.usuario == user:
            raise ValidationError({'treino':_(f'Pk inválido "{treino_model.id}" - objeto não existe.')})
        return value
    
class TreinoCompartilhadoSerializerRetrieve(serializers.ModelSerializer):
    videos = VideosSerializer(many=True,read_only=True)
    class Meta:
        model = TreinosCompartilhadosModel
        fields = ['id','treino','videos','ordem','slug']

class TreinoCompartilhadoSerializerAdd(serializers.Serializer):
    slug_compartilhado = serializers.SlugRelatedField(
        queryset=TreinosCompartilhadosModel.objects.all(),
        slug_field='slug'
        )
    
    class Meta:
        fields = ['slug_compartilhado',]

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        usuario = self.context['request'].user
        treino_compartilhado = ret['slug_compartilhado']
        treino_videos = TreinoVideosmodel.objects.filter(
            usuario=usuario,
            slug_compartilhado = treino_compartilhado.slug
            ).exists()
        
        if treino_videos:
            raise ValidationError({'slug_compartilhado':'Treino adicionado.'})
        return ret