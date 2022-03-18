from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token


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
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        data_login = {
            "username": "test6",
            "email": "",
            "password": "Test123456/"
        }
        response = self.client.post("/api/rest-auth/login/", data_login)
        self.assertEquals(response.status_code, status.HTTP_200_OK)


class UsersApiTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.rest_auth_user_uri = '/api/rest-auth/user/'
        super().setUpClass()

    def setUp(self):
        self.user = User.objects.create_user(
            username="test6",
            password="Test123456/",
        )
        self.token = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)
        print(self.token)

    def test_get_user(self):
        response = self.client.get(self.rest_auth_user_uri)
        self.assertEqual(
            response.data,
            {'pk': self.user.id, 'username': self.user.username, 'email': '', 'first_name': '', 'last_name': ''}
        )





