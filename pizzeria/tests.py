import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

from pizzeria.models import Pizza, Restaurant, Topping
from pizzeria.serializers import \
    PizzaSerializer, RestaurantUpdateSerializer, RestaurantCreateSerializer, RestaurantSerializer, ToppingSerializer


class RegistrationLoginTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test6",
            # email="test123456@test.pl",
            password="Test123456/",
        )
        self.token = Token.objects.create(user=self.user)

    def test_registration(self):

        data_registration = {
            "username": "test5",
            "email": "test12345@test.pl",
            "password1": "Test/12345",
            "password2": "Test/12345"
        }
        response = self.client.post("/api/rest-auth/registration/", data_registration)
        # response = self.client.post("api/rest-auth/login/")
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        data_login = {
            "username": "test6",
            "email": "",
            "password": "Test123456/"
        }
        response = self.client.post("/api/rest-auth/login/", data_login)
        # response = self.client.post("api/rest-auth/login/")
        self.assertEquals(response.status_code, status.HTTP_200_OK)


class RestaurantViewSetTestCase(APITestCase):
    list_url = reverse("restaurant-list")

    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="dominimum",
            address="wolska 3",
            phone_number=555,
        )

    def test_add_restaurant(self):
        data_new_restaurant = {
            "name": "testowa restauracja",
            "address": "dwadaw",
            "phone_number": 55,
            "pizzas": [],
        }
        response = self.client.post("/api/restaurants/", data_new_restaurant)
        # response = self.client.post("api/rest-auth/login/")
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)


    # zrobic update, delete, retrieve, etc.