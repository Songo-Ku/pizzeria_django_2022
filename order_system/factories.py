import factory
from factory import fuzzy  # this line is required from some technical reasons
# from phonenumbers import PhoneNumber
# import phonenumber_field.phonenumber


import faker
from . import models
from django.contrib.auth.models import User
from random import choice as random_choice
from pizzeria.factories import UserFactory, PizzaFactory
from phonenumber_field.modelfields import PhoneNumberField
from faker import Faker

from phonenumbers import PhoneNumber
from random import randint


from phonenumber_field.phonenumber import PhoneNumber


TYPE_OF_PAYMENT = [
    ('not accepted', 'not accepted'),
    ('pending', 'pending'),
    ('accepted', 'accepted')
]


def fake_phone_number(fake: Faker) -> str:
    return f'+48{fake.msisdn()[4:]}'


def generate_phone_number():
    fake = Faker()
    return fake_phone_number(fake)


class ContactUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ContactUser

    address_delivery = 'mordor 2'
    name = factory.Sequence(lambda n: 'user' + str(n))
    surname = 'Kowalski'

    @factory.lazy_attribute
    def phone(self):
        # print('generator\n', generate_phone_number(), '\n')
        phone_n = PhoneNumber.from_string(phone_number=generate_phone_number(), region='PL').as_e164
        # print('phone_n\n', phone_n, '\n')
        return generate_phone_number()


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


# alt_traffic_source = factory.fuzzy.FuzzyChoice(['XYZ', 'ABC', '123', '456'])
# https://stackoverflow.com/questions/62724145/choosing-from-a-list-of-names-using-factory-boy-integrated-with-faker