import factory
from . import models
from django.contrib.auth.models import User
from random import choice as random_choice
from pizzeria.factories import UserFactory, PizzaFactory

TYPE_OF_PAYMENT = [
    ('not accepted', 'not accepted'),
    ('pending', 'pending'),
    ('accepted', 'accepted')
]


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Order

    total = factory.Faker('random_int')
    id_restaurant = 1  # jak zdefiniowac to pole zeby testy przeszly pomyslnie ??
    # dobrze jakby byla fabryka Restauracji zeby w razie dalszych sprawdzen nie był to random number =100 i nie bylo realnie takiej restauracji


class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Payment

    status = random_choice(TYPE_OF_PAYMENT)
    order = factory.SubFactory(OrderFactory)


class OrderedProductsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.OrderedProducts

    pizza_name = factory.Faker('name')
    count = factory.Faker('random_int')
    total = random_choice([30, 50, 70, 100])
    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(PizzaFactory)
