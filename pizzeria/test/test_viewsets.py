from django.utils.html import escape
from pizzeria.forms import EMPTY_ITEM_ERROR

from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, APIClient, URLPatternsTestCase
from rest_framework import status
from rest_framework import routers

from django.urls import path, include, reverse
from pizzeria.views import RestaurantViewSet
from pizzeria.models import Pizza, Restaurant, Topping
from pizzeria.serializers import \
    PizzaSerializer, RestaurantUpdateSerializer, RestaurantCreateSerializer, RestaurantSerializer, ToppingSerializer


class RestaurantViewSetTestCase(APITestCase):
    # list_url = reverse("restaurant-list")
    def setUp(self):
        self.user = User.objects.create(username="nerd")
        self.client.force_authenticate(user=self.user)
        self.restaurant_name = "dominimum"
        self.restaurant_address = "wolska 3"
        self.restaurant_phone_number = 555

    def post_correct_input_restaurant(self):
        valid_restaurant = {
            "name": self.restaurant_name,
            "address": self.restaurant_address,
            "phone_number": self.restaurant_phone_number,
        }
        return self.client.post(f'/api/restaurants/', data=valid_restaurant)

    def post_incorrect_input_restaurant(self):
        invalid_restaurant = {"name": "", "address": "dwadaw", "phone_number": 'dwdaawd',}
        return self.client.post(f'/api/restaurants/', data=invalid_restaurant)

    def test_status_add_correct_restaurant(self):
        response = self.post_correct_input_restaurant()
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_status_add_incorrect_restaurant(self):
        response = self.post_incorrect_input_restaurant()
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_correct_input_restaurant_saved_to_db(self):
        response = self.post_correct_input_restaurant()
        self.assertEquals(Restaurant.objects.count(), 1)
        self.assertEqual(Restaurant.objects.get().name, self.restaurant_name)

    def test_post_incorrect_input_restaurant_saved_to_db(self):
        response = self.post_incorrect_input_restaurant()
        self.assertEquals(Restaurant.objects.count(), 0)

    def test_get_list_restaurants(self):
        url = reverse('restaurant-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(Restaurant.objects.get(id=self.restaurant.id).name, self.restaurant.name)
