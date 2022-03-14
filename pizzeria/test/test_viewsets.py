from django.utils.html import escape
from django.contrib.auth.models import User
from django.urls import path, include, reverse

from pizzeria.forms import EMPTY_ITEM_ERROR
from pizzeria.views import RestaurantViewSet
from pizzeria.models import Pizza, Restaurant, Topping
from pizzeria.serializers import \
    PizzaSerializer, RestaurantUpdateSerializer, RestaurantCreateSerializer, RestaurantSerializer, ToppingSerializer

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, APIClient, URLPatternsTestCase
from rest_framework import status
from rest_framework import routers


from pizzeria.factories import UserFactory, RestaurantFactory


class RestaurantViewSetTestCase(APITestCase):
    restaurant_detail_url = '/api/restaurants/{}/'

    @classmethod
    def setUpClass(cls):
        cls.restaurant_list_url = reverse("restaurant-list")
        cls.user1 = UserFactory()
        cls.restaurant1 = RestaurantFactory(owner=cls.user1)
        print('to jest UserFactory \n', cls.user1)
        super().setUpClass()

    def setUp(self):
        # self.user = User.objects.create(username="nerd")
        self.client.force_authenticate(user=self.user1)
        self.restaurant_name = "dominimum"
        self.restaurant_address = "wolska 3"
        self.restaurant_phone_number = 555
        self.amount = Restaurant.objects.count()

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
        self.assertEquals(Restaurant.objects.count(), 2)
        self.assertEqual(Restaurant.objects.get(name=self.restaurant_name).name, self.restaurant_name)

    def test_post_incorrect_input_restaurant_saved_to_db(self):
        response = self.post_incorrect_input_restaurant()
        self.assertEquals(Restaurant.objects.count(), 1)

    def test_get_list_restaurants(self):
        response = self.client.get(self.restaurant_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(Restaurant.objects.get(id=self.restaurant1.id).name, self.restaurant1.name)

    # tdd assumptions
    def test_get_restaurant_detail_status(self):
        restaurant_ = Restaurant.objects.create(
            name=self.restaurant_name,
            address=self.restaurant_address,
            phone_number=self.restaurant_phone_number,
            owner=self.user1
        )
        response = self.client.get(self.restaurant_detail_url.format(restaurant_.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('owner'), self.user1.id)
        self.assertEqual(response.data.get('pk'), restaurant_.id)
        self.assertEqual(response['content-type'], 'application/json')









































#
# class PizzaAPITest(TestCase):
#     base_url = reverse('item-list')
#
#     def test_POSTing_a_new_item(self):
#         list_ = List.objects.create()
#         response = self.client.post(
#             self.base_url,
#             {'list': list_.id, 'text': 'new item'},
#         )
#         self.assertEqual(response.status_code, 201)
#         new_item = list_.item_set.get()
#         self.assertEqual(new_item.text, 'new item')
#
#
#     def post_empty_input(self):
#         list_ = List.objects.create()
#         return self.client.post(
#             self.base_url,
#             data={'list': list_.id, 'text': ''},
#         )
#
#
#     def test_for_invalid_input_nothing_saved_to_db(self):
#         self.post_empty_input()
#         self.assertEqual(Item.objects.count(), 0)
#
#
#     def test_for_invalid_input_returns_error_code(self):
#         response = self.post_empty_input()
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(
#             json.loads(response.content.decode('utf8')),
#             {'text': [EMPTY_ITEM_ERROR]}
#         )
#
#
#     def test_duplicate_items_error(self):
#         list_ = List.objects.create()
#         self.client.post(self.base_url.format(list_.id), data={
#             'list': list_.id, 'text': 'thing'
#         })
#         response = self.client.post(self.base_url.format(list_.id), data={
#             'list': list_.id, 'text': 'thing'
#         })
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(
#             json.loads(response.content.decode('utf8')),
#             {'non_field_errors': [DUPLICATE_ITEM_ERROR]}
#         )
