from django.utils.html import escape
from pizzeria.forms import EMPTY_ITEM_ERROR

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from rest_framework import status

from pizzeria.models import Pizza, Restaurant, Topping
from pizzeria.serializers import \
    PizzaSerializer, RestaurantUpdateSerializer, RestaurantCreateSerializer, RestaurantSerializer, ToppingSerializer


class AccesToViewSetWithoutLoggedTestCase(APITestCase):
    def test_get_list_restaurants(self):
        url_restaurant = reverse('restaurant-list')
        response = self.client.get(url_restaurant)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_list_toppings(self):
        url_topping = reverse('topping-list')
        response = self.client.get(url_topping)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_pizza(self):
        url_pizza = reverse('pizza-list')
        response = self.client.get(url_pizza)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

