from rest_framework.test import APITestCase
from random import randint
from django.db.models import Max
from order_system.models import Order, ContactUser
from django.urls import reverse
from order_system.models import Order, OrderedProducts, Payment
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

from order_system.factories import OrderFactory, PaymentFactory, OrderedProductsFactory, \
    ContactUserFactory
from pizzeria.factories import UserFactory, RestaurantFactory


import factory
# import phonenumber_field.phonenumber
# phonenumber_field.phonenumber()

from phonenumber_field import phonenumber
from phonenumbers import PhoneNumber
from random import randint
phonen = PhoneNumber(country_code=randint(1, 999), national_number=randint(10000000, 9999999990))
phonen.national_number


class ContactUserViewSetTestCase(APITestCase):
    order_detail_uri = '/api/contact-users/{}/'

    @classmethod
    def setUpClass(cls):
        cls.order_list_url = reverse("contact-user-list")
        cls.user1 = UserFactory()
        cls.contact_user1 = ContactUserFactory()
        super().setUpClass()

    def setUp(self):
        self.client.force_authenticate(user=self.user1)
        self.amount_contact_user = ContactUser.objects.filter().aggregate(max_id=Max('pk')).get('max_id')

    def post_incorrect_contact_user(self):
        invalid_contact_user = {"name": "", "address_delivery": "dwadaw", "phone": 'dwdaawd', "surname": 'cos'}
        return self.client.post(self.order_list_url, data=invalid_contact_user)

    def post_correct_contact_user(self):
        valid_contact_user = {
            "name": 'Janusz',
            "surname": 'Kowalskiii',
            "phone": '+48500444333',
            "address_delivery": 'miejska 16/18'
        }
        return self.client.post(self.order_list_url, data=valid_contact_user)

    def test_add_incorrect_contact_user_status_400(self):
        response = self.post_incorrect_contact_user()
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_contact_user_saved_to_db(self):
        response = self.post_correct_contact_user()
        self.assertEquals(ContactUser.objects.count(), self.amount_contact_user + 1)
        self.assertEqual(ContactUser.objects.get(id=self.amount_contact_user + 1).name, 'Janusz')
        self.assertEqual(response.data.get("name"), 'Janusz')

    def test_post_incorrect_contact_user_not_saved_to_db(self):
        response = self.post_incorrect_contact_user()
        self.assertEquals(ContactUser.objects.count(), self.amount_contact_user)

    def test_status_add_contact_user(self):
        response = self.post_correct_contact_user()
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_get_list_contact_users(self):
        response = self.client.get(self.order_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ContactUser.objects.count(), self.amount_contact_user)
        self.assertEqual(ContactUser.objects.get(id=self.contact_user1.id).name, self.contact_user1.name)

    def test_get_contact_user_detail_status(self):
        contact_user_ = ContactUserFactory(
            # address_delivery='mordororu 33',
            # name='Januszek',
            # surname='Kowalsky',
            # phone='+48516000333',
        )
        user_contact_from_obj = ContactUser.objects.get(id=contact_user_.id)

        phone_faker_factory = phonenumber.PhoneNumber()
        print('faker phone factory: \n', phone_faker_factory)
        print('user conact telephone,\n', user_contact_from_obj.phone)
        response = self.client.get(self.order_detail_uri.format(contact_user_.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), contact_user_.id)
        self.assertEqual(response.data.get('surname'), contact_user_.surname)
        self.assertEqual(response['content-type'], 'application/json')


    # def test_for_not_existed_restaurant(self):
    #     response = self.client.get(self.restaurant_detail_uri.format(self.amount_restaurants + 1))
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#
# class OrderViewSetTestCase(APITestCase):
#     order_detail_uri = '/api/orders/{}/'
#
#     @classmethod
#     def setUpClass(cls):
#         cls.order_list_url = reverse("order-list")
#         cls.user1 = UserFactory()
#         cls.restaurant1 = RestaurantFactory(owner=cls.user1)
#         cls.order1 = OrderFactory()
#         cls.restaurant_list_url = reverse("restaurant-list")
#         cls.user1 = UserFactory()
#         cls.restaurant1 = RestaurantFactory(owner=cls.user1)
#         super().setUpClass()
#
#     def setUp(self):
#         # self.user = User.objects.create(username="nerd")
#         self.client.force_authenticate(user=self.user1)
#         self.restaurant_name = "dominimum"
#         self.restaurant_address = "wolska 3"
#         self.restaurant_phone_number = 555
#         self.amount_restaurants = Restaurant.objects.filter().aggregate(max_id=Max('pk')).get('max_id')
#
#     def post_correct_input_restaurant(self):
#         valid_restaurant = {
#             "name": self.restaurant_name,
#             "address": self.restaurant_address,
#             "phone_number": self.restaurant_phone_number,
#             "owner": self.user1,
#         }
#         return self.client.post(self.restaurant_list_url, data=valid_restaurant)
#
#     def post_incorrect_input_restaurant(self):
#         invalid_restaurant = {"name": "", "address": "dwadaw", "phone_number": 'dwdaawd',}
#         return self.client.post(self.restaurant_list_url, data=invalid_restaurant)
#
#     def test_status_add_correct_restaurant(self):
#         response = self.post_correct_input_restaurant()
#         self.assertEquals(response.status_code, status.HTTP_201_CREATED)
#
#     def test_add_incorrect_restaurant_status_400(self):
#         response = self.post_incorrect_input_restaurant()
#         self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_post_correct_input_restaurant_saved_to_db(self):
#         self.post_correct_input_restaurant()
#         self.assertEquals(Restaurant.objects.count(), self.amount_restaurants + 1)  # czy tak powinno się robić czy na sztywno?
#         self.assertEqual(Restaurant.objects.get(name=self.restaurant_name).name, self.restaurant_name)
#
#     def test_post_incorrect_input_restaurant_saved_to_db(self):
#         response = self.post_incorrect_input_restaurant()
#         self.assertEquals(Restaurant.objects.count(), self.amount_restaurants)
#
#     def test_get_list_restaurants(self):
#         response = self.client.get(self.restaurant_list_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Restaurant.objects.count(), self.amount_restaurants)
#         self.assertEqual(Restaurant.objects.get(id=self.restaurant1.id).name, self.restaurant1.name)
#
#     # tdd assumptions
#     def test_get_restaurant_detail_status(self):
#         restaurant_ = RestaurantFactory(owner=self.user1)
#         response = self.client.get(self.restaurant_detail_uri.format(restaurant_.id))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data.get('owner'), self.user1.id)
#         self.assertEqual(response.data.get('pk'), restaurant_.id)
#         self.assertEqual(response['content-type'], 'application/json')
#
#     def test_for_not_existed_restaurant(self):
#         response = self.client.get(self.restaurant_detail_uri.format(self.amount_restaurants + 1))
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)