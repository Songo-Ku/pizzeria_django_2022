from random import randint

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
        response = self.post_correct_input_restaurant()
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
        cls.pizza_list_url = reverse("topping-list")
        cls.user1 = UserFactory()
        cls.restaurant1 = RestaurantFactory(owner=cls.user1)
        cls.pizza1 = PizzaFactory(restaurant=cls.restaurant1)
        print('cls pizza1: \n', cls.pizza1, '\n')
        # cls.topping1 = ToppingFactory()
        cls.topping1 = ToppingFactory.create(meals=(cls.pizza1))



        print('\n to topping1:       ', cls.topping1)
        print('\n to meals z topping1:       ', cls.topping1.meals)

        print('to jest UserFactory \n', cls.user1)
        super().setUpClass()

    def setUp(self):
        self.client.force_authenticate(user=self.user1)
        self.topping_name = "capri"
        self.topping_price = randint(20, 45)
        # self.description = factory.Sequence(lambda n: 'losowy opis nr %d' % n)
        self.topping_supplier = ' to opis topping '
        self.amount_toppings = Topping.objects.count()
        print('amount pizza: ', self.amount_toppings)

    def test_for_not_existed_topping(self):
        response = self.client.get(self.topping_detail_uri.format(self.amount_toppings + 1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #
    # def post_correct_input_pizza(self):
    #     valid_pizza = {
    #         "name": self.pizza_name,
    #         "price": self.pizza_price,
    #         "description": self.pizza_description,
    #         "restaurant": self.restaurant3.id,
    #     }
    #     return self.client.post(self.pizza_list_url, data=valid_pizza)
    #
    # def post_incorrect_input_pizza(self):
    #     invalid_pizza = {"name": "", "price": "dwadaw", "description": 'dwdaawd',}
    #     return self.client.post(self.pizza_list_url, data=invalid_pizza)
    #
    # def test_incorrect_post_pizza_status_400(self):
    #     response = self.post_incorrect_input_pizza()
    #     self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
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



































