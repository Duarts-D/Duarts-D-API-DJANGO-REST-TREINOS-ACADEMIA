from factory import django
from apps.academia import models
from faker import Faker
from factory import SubFactory
import factory

fake = Faker()

class EquipamentoFactory(django.DjangoModelFactory):
    class Meta:
        model = models.EquipamentoModel

    equipamento = factory.Faker('first_name')

class GrupoMuscularFactory(django.DjangoModelFactory):
    class Meta:
        model = models.GrupoMuscularModel

    grupo_muscular = factory.Faker('first_name')


class VideosFactory(django.DjangoModelFactory):
    class Meta:
        model = models.VideoModel
    
    video_nome = factory.Faker('name')
    video_id_youtube = fake.name()
    video_url = fake.name()
    informacao = fake.text()
    # imagem = ''
    video_id_didatico = ''
    grupo_muscular = SubFactory(GrupoMuscularFactory)
    equipamento = SubFactory(EquipamentoFactory)
    publicado = True

class TreinoCompartilhadoFactory(django.DjangoModelFactory):
    class Meta:
        model = models.TreinosCompartilhadosModel
        skip_postgeneration_save = True
    treino = factory.sequence(lambda n: f'Treino-{n}')
    ordem =  '[1,2,3]'
    slug = factory.sequence(lambda n: f'Treino{n}')
    videos = factory.Sequence(lambda n: n )

    @factory.post_generation
    def videos(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.videos.add(*extracted)