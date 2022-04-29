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
from order_system.serializers import PaymentCreateSerializer, PaymentSerializer
from pizzeria.factories import UserFactory, RestaurantFactory, PizzaFactory
import json


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
        contact_user_ = ContactUserFactory()  # this create and save contact user
        response = self.client.get(self.order_detail_uri.format(contact_user_.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), contact_user_.id)
        self.assertEqual(response.data.get('surname'), contact_user_.surname)
        self.assertEqual(response['content-type'], 'application/json')

    def test_for_not_existed_user_contact(self):
        response = self.client.get(self.order_detail_uri.format(self.amount_contact_user + 1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class OrderViewSetTestCase(APITestCase):
    order_detail_uri = '/api/orders/{}/'

    @classmethod
    def setUpClass(cls):
        cls.contact_user1 = ContactUserFactory()
        cls.contact_user2 = ContactUserFactory()

        cls.order_list_url = reverse("order-list")
        cls.user1 = UserFactory()
        cls.restaurant1 = RestaurantFactory(owner=cls.user1)
        cls.restaurant2 = RestaurantFactory(owner=cls.user1)

        cls.order1 = OrderFactory(restaurant=cls.restaurant1, contact_user=cls.contact_user1)
        # cls.restaurant_list_url = reverse("restaurant-list")
        cls.restaurant1 = RestaurantFactory(owner=cls.user1)
        super().setUpClass()

    def setUp(self):
        self.client.force_authenticate(user=self.user1)
        self.amount_order = Order.objects.filter().aggregate(max_id=Max('pk')).get('max_id')

    def post_correct_input_order(self):
        valid_order = {
            "restaurant": self.restaurant1.id,
            "contact_user": self.contact_user1.id
        }
        return self.client.post(self.order_list_url, data=valid_order)

    def post_incorrect_input_order(self):
        invalid_restaurant = {"contact_user": "wrong data", "restaurant": "wrong data"}
        return self.client.post(self.order_list_url, data=invalid_restaurant)

    def test_status_add_correct_order(self):
        response = self.post_correct_input_order()
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_post_correct_input_order_saved_to_db(self):
        response = self.post_correct_input_order()
        self.assertEquals(Order.objects.count(), self.amount_order + 1)
        self.assertEqual(response.data.get('ordered_products'), [])
        self.assertEqual(Order.objects.get(pk=response.data.get("pk")).restaurant.id, self.restaurant1.id)

    def test_post_incorrect_input_order_saved_to_db(self):
        response = self.post_incorrect_input_order()
        self.assertEquals(Order.objects.count(), self.amount_order)

    def test_add_incorrect_order_status_400(self):
        response = self.post_incorrect_input_order()
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_list_order(self):
        response = self.client.get(self.order_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.count(), self.amount_order)
        self.assertEqual(Order.objects.get(id=self.order1.id).restaurant, self.order1.restaurant)

    # tdd assumptions
    def test_get_order_detail_status(self):
        order_ = OrderFactory(restaurant=self.restaurant2, contact_user=self.contact_user2)
        response = self.client.get(self.order_detail_uri.format(order_.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('contact_user'), self.contact_user2.id)
        self.assertEqual(response.data.get('restaurant'), self.restaurant2.id)
        self.assertEqual(response.data.get('pk'), order_.id)
        self.assertEqual(response['content-type'], 'application/json')

    def test_for_not_existed_order(self):
        response = self.client.get(self.order_detail_uri.format(self.amount_order + 1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PaymentViewSetTestCase(APITestCase):
    payment_detail_uri = '/api/payments/{}/'

    @classmethod
    def setUpClass(cls):
        cls.user1 = UserFactory()
        cls.url_payment_list = reverse("payment-list")
        cls.restaurant1 = RestaurantFactory(owner=cls.user1)
        cls.user_contact1 = ContactUserFactory()
        cls.order1 = OrderFactory(restaurant=cls.restaurant1, contact_user=cls.user_contact1)
        cls.order2 = OrderFactory(restaurant=cls.restaurant1, contact_user=cls.user_contact1)
        cls.payment1 = PaymentFactory(order=cls.order1)
        super().setUpClass()

    def setUp(self):
        self.client.force_authenticate(user=self.user1)
        self.amount_of_payment = Payment.objects.filter().aggregate(max_id=Max('pk')).get('max_id')

    def post_correct_payment(self):
        valid_payment = {
            "order": self.order2.id
        }
        return self.client.post(self.url_payment_list, valid_payment)

    def post_incorrect_payment(self):
        invalid_payment = {
            "order": ""
        }
        return self.client.post(self.url_payment_list, invalid_payment)

    def test_post_payment_status_200(self):
        response = self.post_correct_payment()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_payment_field_input_validation(self):
        response = self.post_correct_payment()
        self.assertEqual(response.data.get('status'), "not accepted")
        self.assertEqual(response.data.get('order'), self.order2.id)

    def test_post_payment_saved_to_db(self):
        self.post_correct_payment()
        self.assertEqual(Payment.objects.count(), self.amount_of_payment + 1)

    def test_post_incorrect_payment_status_400(self):
        response = self.post_incorrect_payment()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_incorrect_payment_not_saved_to_db(self):
        self.post_incorrect_payment()
        self.assertEqual(Payment.objects.count(), self.amount_of_payment)

    def test_post_not_exist_payment_status_404(self):
        response = self.client.get(self.payment_detail_uri.format(self.amount_of_payment + 1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_payments(self):
        response = self.client.get(self.url_payment_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.amount_of_payment)
        data_serializer = PaymentSerializer(self.payment1).data
        data_serializer['status'] = str(data_serializer.get("status"))
        self.assertIn(data_serializer, json.loads(response.content))

    def test_detail_payment(self):
        response = self.client.get(self.payment_detail_uri.format(self.payment1.id))
        self.assertEqual(response.data.get("status"), str(self.payment1.status))
        self.assertEqual(response.data.get("restaurant_name"), str(self.restaurant1.name))
        self.assertEqual(response.data.get("restaurant_id"), self.restaurant1.pk)


class OrderedProductViewSetTestCase(APITestCase):
    payment_detail_uri = '/api/order-products/{}/'

    @classmethod
    def setUpClass(cls):
        cls.user1 = UserFactory()
        cls.contact_user1 = ContactUserFactory()
        cls.restaurant1 = RestaurantFactory(owner=cls.user1)
        cls.order1 = OrderFactory(restaurant=cls.restaurant1)
        cls.product1 = PizzaFactory(restaurant=cls.restaurant1)
        cls.product_ordered = OrderedProductsFactory(product=cls.product1, restaurant=cls.restaurant1)
        super().setUpClass()

    def setUp(self):
        self.client.force_authenticate(user=self.user1)
        self.amount_ordered_products = OrderedProducts.objects.filter().aggregate(max_id=Max('pk')).get("max_id")