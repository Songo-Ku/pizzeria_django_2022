from random import randint

from django.db.models import Max
from django.utils.html import escape
from django.contrib.auth.models import User
from django.urls import path, include, reverse
# from faker import factory
from faker import Faker
from faker.providers import DynamicProvider
import factory

from pizzeria.models import Pizza, Restaurant, Topping

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, APIClient, URLPatternsTestCase
from rest_framework import status
from rest_framework import routers

from pizzeria.factories import UserFactory, RestaurantFactory, PizzaFactory, ToppingFactory


name_topping_provider = DynamicProvider(
     provider_name="name_topping",
     elements=["ser", "szynka", "pieczarki", "ananas", "boczek"],
)


class RestaurantViewSetTestCase(APITestCase):
    restaurant_detail_uri = '/api/restaurants/{}/'

    @classmethod
    def setUpClass(cls):
        cls.restaurant_list_url = reverse("restaurant-list")
        cls.user1 = UserFactory()
        cls.restaurant1 = RestaurantFactory(owner=cls.user1)
        super().setUpClass()

    def setUp(self):
        # self.user = User.objects.create(username="nerd")
        self.client.force_authenticate(user=self.user1)
        self.restaurant_name = "dominimum"
        self.restaurant_address = "wolska 3"
        self.restaurant_phone_number = 555
        self.amount_restaurants = Restaurant.objects.count()

    def post_correct_input_restaurant(self):
        valid_restaurant = {
            "name": self.restaurant_name,
            "address": self.restaurant_address,
            "phone_number": self.restaurant_phone_number,
            "owner": self.user1,
        }
        return self.client.post(self.restaurant_list_url, data=valid_restaurant)

    def post_incorrect_input_restaurant(self):
        invalid_restaurant = {"name": "", "address": "dwadaw", "phone_number": 'dwdaawd',}
        return self.client.post(self.restaurant_list_url, data=invalid_restaurant)

    def test_status_add_correct_restaurant(self):
        response = self.post_correct_input_restaurant()
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_add_incorrect_restaurant_status_400(self):
        response = self.post_incorrect_input_restaurant()
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_correct_input_restaurant_saved_to_db(self):
        self.post_correct_input_restaurant()
        # max_id = Restaurant.objects.aggregate(Max('id'))
        self.assertEquals(Restaurant.objects.count(), self.amount_restaurants + 1)  # czy tak powinno się robić czy na sztywno?
        self.assertEqual(Restaurant.objects.get(name=self.restaurant_name).name, self.restaurant_name)

    def test_post_incorrect_input_restaurant_saved_to_db(self):
        response = self.post_incorrect_input_restaurant()
        self.assertEquals(Restaurant.objects.count(), self.amount_restaurants)

    def test_get_list_restaurants(self):
        response = self.client.get(self.restaurant_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Restaurant.objects.count(), self.amount_restaurants)
        self.assertEqual(Restaurant.objects.get(id=self.restaurant1.id).name, self.restaurant1.name)

    # tdd assumptions
    def test_get_restaurant_detail_status(self):
        restaurant_ = RestaurantFactory(owner=self.user1)
        response = self.client.get(self.restaurant_detail_uri.format(restaurant_.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('owner'), self.user1.id)
        self.assertEqual(response.data.get('pk'), restaurant_.id)
        self.assertEqual(response['content-type'], 'application/json')

    def test_for_not_existed_restaurant(self):
        response = self.client.get(self.restaurant_detail_uri.format(self.amount_restaurants + 1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PizzaViewSetTestCase(APITestCase):
    pizza_detail_uri = '/api/pizzas/{}/'

    @classmethod
    def setUpClass(cls):
        cls.pizza_list_url = reverse("pizza-list")
        cls.user2 = UserFactory()
        cls.restaurant2 = RestaurantFactory(owner=cls.user2)
        cls.restaurant3 = RestaurantFactory(owner=cls.user2)
        cls.pizza1 = PizzaFactory(restaurant=cls.restaurant2)
        # print(cls.pizza1, '\n to pizza1')
        # print('to jest UserFactory \n', cls.user2)
        super().setUpClass()

    def setUp(self):
        self.client.force_authenticate(user=self.user2)
        self.pizza_name = "capri"
        self.pizza_price = randint(20, 45)
        # self.description = factory.Sequence(lambda n: 'losowy opis nr %d' % n)
        self.pizza_description = ' dupa opis pizzy'
        self.amount_pizzas = Pizza.objects.count()
        # print('amount pizza: ', self.amount_pizzas)

    def test_for_not_existed_pizza(self):
        response = self.client.get(self.pizza_detail_uri.format(self.amount_pizzas + 1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def post_correct_input_pizza(self):
        valid_pizza = {
            "name": self.pizza_name,
            "price": self.pizza_price,
            "description": self.pizza_description,
            "restaurant": self.restaurant3.id,
        }
        return self.client.post(self.pizza_list_url, data=valid_pizza)

    def post_incorrect_input_pizza(self):
        invalid_pizza = {"name": "", "price": "dwadaw", "description": 'dwdaawd',}
        return self.client.post(self.pizza_list_url, data=invalid_pizza)

    def test_incorrect_post_pizza_status_400(self):
        response = self.post_incorrect_input_pizza()
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_incorrect_restaurant_not_saved_to_db(self):
        response = self.post_incorrect_input_pizza()
        self.assertEquals(Pizza.objects.count(), self.amount_pizzas)

    def test_post_correct_pizza_status_201(self):
        response = self.post_correct_input_pizza()
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_post_correct_pizza_saved_to_db(self):
        response = self.post_correct_input_pizza()
        self.assertEquals(Pizza.objects.count(), self.amount_pizzas + 1)
        self.assertEqual(Pizza.objects.get(name=self.pizza_name).name, self.pizza_name)

    def test_get_list_pizzas_status_200(self):
        response = self.client.get(self.pizza_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def pizza_object_exist_after_init(self):
        self.assertEqual(Pizza.objects.get(id=self.pizza1.id).name, self.pizza1.name)

    def test_get_pizza_detail_status(self):
        response = self.client.get(self.pizza_detail_uri.format(self.pizza1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_pizza_detail_correct_data_json(self):
        response = self.client.get(self.pizza_detail_uri.format(self.pizza1.id))
        self.assertEqual(response.data.get('name'), self.pizza1.name)
        self.assertEqual(response.data.get('pk'), self.pizza1.id)
        self.assertEqual(response.data.get('restaurant'), self.restaurant2.id)
        self.assertEqual(response['content-type'], 'application/json')


class ToppingViewSetTestCase(APITestCase):
    topping_detail_uri = '/api/toppings/{}/'

    @classmethod
    def setUpClass(cls):
        cls.topping_list_url = reverse("topping-list")
        cls.user1 = UserFactory()
        cls.restaurant1 = RestaurantFactory(owner=cls.user1)
        cls.pizza1 = PizzaFactory(restaurant=cls.restaurant1)
        cls.pizza2 = PizzaFactory(restaurant=cls.restaurant1)

        cls.topping1 = ToppingFactory.create(meals=[cls.pizza1.id, cls.pizza2.id])
        cls.topping2 = ToppingFactory.create(meals=[cls.pizza2])
        cls.topping_faker1 = Faker()
        Faker.seed(321)
        cls.topping_faker1.add_provider(name_topping_provider)  # customowy faker z nazwa skladnika
        super().setUpClass()

    def setUp(self):
        self.client.force_authenticate(user=self.user1)
        # self.description = factory.Sequence(lambda n: 'losowy opis nr %d' % n)
        self.amount_toppings = Topping.objects.count()
        # self.max_id = Restaurant.objects.aggregate(Max('id'))
        self.max_id = Restaurant.objects.filter().aggregate(max_id=Max('pk'))
        self.maxid_2 = Restaurant.objects.aggregate(Max('pk')).get('pk__max')
        print(' maxid2222  \n', self.maxid_2)

        self.max_id = self.max_id.get('max_id')
        self.amount_restaurant = Restaurant.objects.count()
        print(self.amount_restaurant, 'to jest amount restaurant z count \n')
        print(self.max_id, ' to jest max id \n')
        self.topping1.refresh_from_db()
        print('\n to meals z topping1:       ', self.topping1.meals)

    def test_for_not_existed_topping(self):
        response = self.client.get(self.topping_detail_uri.format(self.amount_toppings + 1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def post_correct_input_topping(self):
        valid_topping = {
            "name": self.topping_faker1.name_topping(),
            "price": self.randint(20, 45),
            "supplier": self.topping_faker1.text(),
            "meals": [self.pizza1.id, self.pizza2.id],
        }
        return self.client.post(self.topping_list_url, data=valid_topping)

    def post_incorrect_input_topping(self):
        invalid_topping = {"name": "", "price": "dwadaw", "supplier": 'dwdaawd',}
        return self.client.post(self.topping_list_url, data=invalid_topping)

    def test_incorrect_post_pizza_status_400(self):
        response = self.post_incorrect_input_topping()
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_post_incorrect_restaurant_not_saved_to_db(self):
    #     response = self.post_incorrect_input_pizza()
    #     self.assertEquals(Pizza.objects.count(), self.amount_pizzas)
    #
    # def test_post_correct_pizza_status_201(self):
    #     response = self.post_correct_input_pizza()
    #     self.assertEquals(response.status_code, status.HTTP_201_CREATED)
    #
    # def test_post_correct_pizza_saved_to_db(self):
    #     response = self.post_correct_input_pizza()
    #     self.assertEquals(Pizza.objects.count(), self.amount_pizzas + 1)
    #     self.assertEqual(Pizza.objects.get(name=self.pizza_name).name, self.pizza_name)
    #
    # def test_get_list_pizzas_status_200(self):
    #     response = self.client.get(self.pizza_list_url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def pizza_object_exist_after_init(self):
    #     self.assertEqual(Pizza.objects.get(id=self.pizza1.id).name, self.pizza1.name)
    #
    # def test_get_pizza_detail_status(self):
    #     response = self.client.get(self.pizza_detail_uri.format(self.pizza1.id))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_get_pizza_detail_correct_data_json(self):
    #     response = self.client.get(self.pizza_detail_uri.format(self.pizza1.id))
    #     self.assertEqual(response.data.get('name'), self.pizza1.name)
    #     self.assertEqual(response.data.get('pk'), self.pizza1.id)
    #     self.assertEqual(response.data.get('restaurant'), self.restaurant2.id)
    #     self.assertEqual(response['content-type'], 'application/json')
    #
    #

class TiestooooViewSetTestCase(APITestCase):
    topping_detail_uri = '/api/xxxx/{}/'

    @classmethod
    def setUpClass(cls):
        cls.maxid_2 = Restaurant.objects.all().aggregate(Max('pk')).get('pk__max')
        print(cls.maxid_2, ' max id 2 dla iestooottotototototo \n')
        cls.objlast = Restaurant.objects.last()
        print(cls.objlast.id, ' obj last')
        cls.restaurant_list_url = reverse("restaurant-list")
        super().setUpClass()

    def test_get_list_restaurants(self):
        response = self.client.get(self.restaurant_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

























