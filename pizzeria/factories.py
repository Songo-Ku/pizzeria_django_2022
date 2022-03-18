import factory
from . import models
from django.contrib.auth.models import User
from random import randint, choice


TYPE_OF_PIZZA = ['margerita', 'hawai', 'capriciosa', 'kebab', 'fivecheese']
TOPPING = ['cheese', 'pineaple', 'cham', 'salami', 'tomato souce']



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


class PizzaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Pizza

    name = choice(TYPE_OF_PIZZA)  # + str(factory.Sequence(lambda n: ' %d' % n))
    price = randint(20, 45)
    description = factory.Sequence(lambda n: 'losowy opis nr %d' % n)
    restaurant = factory.SubFactory(RestaurantFactory)


class ToppingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Topping

    name = choice(TOPPING) + str(factory.Sequence(lambda n: 'skladnik o nr. %d' % n))
    price = randint(20, 45)
    supplier = factory.Sequence(lambda n: 'random supplier id %d' % n)

    @factory.post_generation
    def meals(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for meal in extracted:
                self.meals.add(meal)






# class ToppingPizzaFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = models.PizzaTopping
#
#     topping = factory.SubFactory(ToppingFactory)
#     pizza = factory.SubFactory(PizzaFactory)






