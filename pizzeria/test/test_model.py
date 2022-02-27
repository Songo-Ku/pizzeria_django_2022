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

    def test_model_can_create_restaurant(self):
        old_count = Restaurant.objects.count()
        self.restaurant.save()
        new_count = Restaurant.objects.count()
        self.assertNotEqual(old_count, new_count)












        # self.valid_restaurant = Restaurant.objects.create(
        #     name=self.restaurant_name,
        #     address=self.restaurant_address,
        #     phone_number=self.restaurant_phone_number,
        # )
        # self.restaurant = Restaurant.objects.create(
        #     name='',
        #     address=self.restaurant_address,
        #     phone_number=self.restaurant_phone_number,
        # )


