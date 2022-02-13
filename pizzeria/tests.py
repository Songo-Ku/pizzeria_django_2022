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


class ModelTestCase(TestCase):
    """This class defines the test suite for the bucketlist model."""

    def setUp(self):
        """Define the test client and other test variables."""
        user = User.objects.create(username="nerd")
        self.restaurant_name = "dominimum"
        self.restaurant_address = "wolska 3"
        self.restaurant_phone_number = 555
        self.restaurant = Restaurant(
            name=self.restaurant_name,
            address=self.restaurant_address,
            phone_number=self.restaurant_phone_number,
        )

    def test_model_can_create_a_bucketlist(self):
        """Test the bucketlist model can create a bucketlist."""
        old_count = Restaurant.objects.count()
        self.restaurant.save()
        new_count = Restaurant.objects.count()
        self.assertNotEqual(old_count, new_count)


class RestaurantViewSetTestCase(APITestCase):
    list_url = reverse("restaurant-list")

    def setUp(self):
        user = User.objects.create(username="nerd")
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.client.force_authenticate(user=user)
        self.restaurant_name = "dominimum"
        self.restaurant_address = "wolska 3"
        self.restaurant_phone_number = 555
        self.restaurant = Restaurant.objects.create(
            name=self.restaurant_name,
            address=self.restaurant_address,
            phone_number=self.restaurant_phone_number,
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
        # test


    # zrobic update, delete, retrieve, etc.