import factory
from django.contrib.auth.hashers import make_password
from faker import Factory

from profiles import models

PASSWORD = "a123321a"

factory_en = Factory.create(
    "En-Us",
    providers=[
        "faker.providers.misc",
        "faker.providers.person",
        "faker.providers.lorem",
        "faker.providers.internet",
    ],
)


class ProfileFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda x: factory_en.user_name())
    description = factory.Sequence(lambda x: factory_en.text())
    password = make_password(PASSWORD)

    class Meta:
        model = models.Profile


class AdminFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda x: factory_en.user_name())
    description = factory.Sequence(lambda x: factory_en.text())
    password = make_password(PASSWORD)

    class Meta:
        model = models.Profile

    is_staff = True
