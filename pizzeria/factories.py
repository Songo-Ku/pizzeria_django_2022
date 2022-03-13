import factory
from . import models
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user%d' % n)


class RestaurantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Restaurant

    name = factory.Sequence(lambda n: 'restauracja%d' % n)
    address = factory.Sequence(lambda n: 'adres%d' % n)
    phone_number = 666
    owner = factory.SubFactory(UserFactory)





