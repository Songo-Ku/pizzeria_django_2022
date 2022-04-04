import factory
from factory import fuzzy  # this line is required from some technical reasons
# from phonenumbers import PhoneNumber
# import phonenumber_field.phonenumber

from . import models
from django.contrib.auth.models import User
from random import choice as random_choice
from pizzeria.factories import UserFactory, PizzaFactory

from phonenumbers import PhoneNumber
from random import randint


# phonen.national_number

TYPE_OF_PAYMENT = [
    ('not accepted', 'not accepted'),
    ('pending', 'pending'),
    ('accepted', 'accepted')
]
# import faker
# faker.Faker.seed(0)
# for _ in range(5):
#     faker.country_calling_code()


class ContactUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ContactUser

    address_delivery = 'mordor 2'
    # do wyboru gdzie moga byc powtorzone = factory.fuzzy.FuzzyChoice(['Magda', 'Marek', 'Arek', 'Janusz', 'Marta'])
    name = factory.Sequence(lambda n: 'user' + n)
    surname = 'Kowalski'
    phone = factory.Faker('phone_number')


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
