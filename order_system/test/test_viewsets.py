from rest_framework.test import APITestCase
from random import randint
from django.db.models import Max
from order_system.models import Order
from django.urls import reverse
from order_system.models import Order, OrderedProducts, Payment
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

from order_system.factories import OrderFactory
from pizzeria.factories import UserFactory, RestaurantFactory


class OrderViewSetTestCase(APITestCase):
    order_detail_uri = '/api/orders/{}/'

    @classmethod
    def setUpClass(cls):
        cls.order_list_url = reverse("order-list")
        cls.user1 = UserFactory()
        cls.restaurant1 = RestaurantFactory(owner=cls.user1)
        cls.order1 = OrderFactory()

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
