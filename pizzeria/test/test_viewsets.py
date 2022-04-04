from random import randint

from django.db.models import Max
from django.utils.html import escape
from django.contrib.auth.models import User
from django.urls import path, include, reverse
# from faker import factory
import factory

from pizzeria.models import Pizza, Restaurant, Topping

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, APIClient, URLPatternsTestCase
from rest_framework import status
from rest_framework import routers

from pizzeria.factories import UserFactory, RestaurantFactory, PizzaFactory, ToppingFactory


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
        self.amount_restaurants = Restaurant.objects.filter().aggregate(max_id=Max('pk')).get('max_id')

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
        self.assertEquals(Restaurant.objects.count(), self.amount_restaurants + 1)
        self.assertEqual(Restaurant.objects.get(name=self.restaurant_name).name, self.restaurant_name)

    def test_post_incorrect_input_restaurant_saved_to_db(self):
        response = self.post_incorrect_input_restaurant()
        self.assertEquals(Restaurant.objects.count(), self.amount_restaurants)

    def test_get_list_restaurants(self):
        response = self.client.get(self.restaurant_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Restaurant.objects.count(), self.amount_restaurants)
        self.assertEqual(Restaurant.objects.get(id=self.restaurant1.id).name, self.restaurant1.name)

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
        super().setUpClass()

    def setUp(self):
        self.client.force_authenticate(user=self.user2)
        self.pizza_name = "capri"
        self.pizza_price = randint(20, 45)
        self.pizza_description = ' dupa opis pizzy'
        self.amount_pizzas = Pizza.objects.filter().aggregate(max_id=Max('pk')).get('max_id')

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
        cls.pizza3 = PizzaFactory(restaurant=cls.restaurant1)
        cls.topping1 = ToppingFactory.create(meals=(cls.pizza1.id, cls.pizza2.id))
        cls.topping2 = ToppingFactory.create(meals=[cls.pizza3])
        cls.topping3 = ToppingFactory()
        super().setUpClass()

    def setUp(self):
        self.client.force_authenticate(user=self.user1)
        self.max_id_topping = Topping.objects.filter().aggregate(max_id=Max('pk')).get('max_id')

    def test_for_not_existed_topping(self):
        response = self.client.get(self.topping_detail_uri.format(self.max_id_topping + 1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def post_correct_input_topping(self):
        valid_topping = {
            "name": self.topping3.name,
            "price": self.topping3.price,
            "supplier": "to jest supplier in test",
            "meals": [],
        }
        return self.client.post(self.topping_list_url, data=valid_topping)

    def post_incorrect_input_topping(self):
        invalid_topping = {"name": "", "price": "dwadaw", "supplier": 'dwdaawd',}
        return self.client.post(self.topping_list_url, data=invalid_topping)

    def test_incorrect_post_topping_status_400(self):
        response = self.post_incorrect_input_topping()
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_incorrect_topping_not_saved_to_db(self):
        self.post_incorrect_input_topping()
        self.assertEquals(Topping.objects.count(), self.max_id_topping)

    def test_post_correct_topping_status_201(self):
        response = self.post_correct_input_topping()
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_post_correct_topping_with_many_meals(self):
        valid_topping_with_meals = {
            "name": self.topping3.name,
            "price": self.topping3.price,
            "supplier": "to jest supplier in test",
            "meals": [self.pizza1.id, self.pizza2.id, self.pizza3.id],
        }
        response = self.client.post(self.topping_list_url, data=valid_topping_with_meals)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Topping.objects.count(), self.max_id_topping + 1)
        self.assertEqual(response.data.get('meals'), [self.pizza1.id, self.pizza2.id, self.pizza3.id])

    def test_post_correct_topping_saved_to_db(self):
        response = self.post_correct_input_topping()
        self.assertEquals(Topping.objects.count(), self.max_id_topping + 1)
        self.assertEqual(Topping.objects.get(id=self.max_id_topping + 1).name, self.topping3.name)

    def test_get_list_toppings_status_200(self):
        response = self.client.get(self.topping_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def topping_object_exist_after_init(self):
        self.assertEqual(Topping.objects.get(id=self.topping1.id).name, self.topping1.name)

    def test_get_topping_detail_status(self):
        response = self.client.get(self.topping_detail_uri.format(self.topping1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_topping_detail_correct_data_json(self):
        response = self.client.get(self.topping_detail_uri.format(self.topping1.id))
        self.assertEqual(response.data.get('name'), self.topping1.name)
        self.assertEqual(response.data.get('pk'), self.topping1.id)
        self.assertEqual(response.data.get('meals'), [topping.id for topping in self.topping1.meals.all()])
        self.assertEqual(response['content-type'], 'application/json')




























