import factory
from factory import fuzzy  # this line is required from some technical reasons
from random import randint
import faker
from . import models
from django.contrib.auth.models import User
from random import choice as random_choice
from pizzeria.factories import UserFactory, PizzaFactory, RestaurantFactory
from faker import Faker

from phonenumbers import PhoneNumber
from phonenumber_field.phonenumber import PhoneNumber


TYPE_OF_PAYMENT = [
    ('not accepted', 'not accepted'),
    ('pending', 'pending'),
    ('accepted', 'accepted')
]


def fake_phone_number(fake: Faker) -> str:
    # started_pl_phone_number = [5, 6, 8]
    # diced_pl_number = started_pl_phone_number[randint(0, 2)]
    # return f'+48{diced_pl_number}{fake.msisdn()[5:]}'
    return f'+48{5}{fake.msisdn()[5:]}'


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
        return generate_phone_number()


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Order

    contact_user = factory.SubFactory(ContactUserFactory)
    restaurant = factory.SubFactory(RestaurantFactory)


class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Payment

    status = factory.fuzzy.FuzzyChoice(TYPE_OF_PAYMENT)
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