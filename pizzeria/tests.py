import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, APIClient

from rest_framework import status

from pizzeria.models import Pizza, Restaurant, Topping
from pizzeria.serializers import \
    PizzaSerializer, RestaurantUpdateSerializer, RestaurantCreateSerializer, RestaurantSerializer, ToppingSerializer




class RestaurantViewSetTestCase(APITestCase):
    list_url = reverse("restaurant-list")

    def post_correct_input_restaurant(self):
        data_new_restaurant = {"name": "testowa restauracja", "address": "dwadaw", "phone_number": 55,}
        return self.client.post(f'/api/restaurants/', data=data_new_restaurant)

    def post_incorrect_input_restaurant(self):
        data_new_restaurant = {"name": "", "address": "dwadaw", "phone_number": 'dwdaawd',}
        return self.client.post(f'/api/restaurants/', data=data_new_restaurant)

    def setUp(self):
        user = User.objects.create(username="nerd")
        # self.factory = APIRequestFactory()
        self.client.force_authenticate(user=user)
        # self.restaurant_name = "dominimum"
        # self.restaurant_address = "wolska 3"
        # self.restaurant_phone_number = 555
        # self.restaurant = Restaurant.objects.create(
        #     name=self.restaurant_name,
        #     address=self.restaurant_address,
        #     phone_number=self.restaurant_phone_number,
        # )

    def test_add_correct_restaurant(self):
        response = self.post_correct_input_restaurant()
        # response = self.client.post("api/rest-auth/login/")
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_add_incorrect_restaurant(self):
        response = self.post_incorrect_input_restaurant()
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

