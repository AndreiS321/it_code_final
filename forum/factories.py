import factory
from faker import Factory

from forum import models
from profiles.factories import ProfileFactory

factory_ru = Factory.create(
    "ru_Ru",
    providers=[
        "faker.providers.misc",
        "faker.providers.lorem",
    ],
)


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda x: factory_ru.word())
    creator = factory.SubFactory(ProfileFactory)

    class Meta:
        model = models.Category


class ThemeFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda x: factory_ru.word())
    creator = factory.SubFactory(ProfileFactory)
    category = factory.SubFactory(CategoryFactory)

    class Meta:
        model = models.Theme


class ThemeMessageFactory(factory.django.DjangoModelFactory):
    text = factory.Sequence(lambda x: factory_ru.word())
    from_user = factory.SubFactory(ProfileFactory)
    theme = factory.SubFactory(ThemeFactory)

    class Meta:
        model = models.ThemeMessage
