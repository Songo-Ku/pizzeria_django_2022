from django.shortcuts import render
# from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import mixins, generics, renderers
from .models import Restaurant, Topping, Pizza
from .serializers import RestaurantSerializer, ToppingSerializer, PizzaSerializer
from rest_framework import viewsets


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()


class ToppingViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = ToppingSerializer
    queryset = Topping.objects.all()


class PizzaViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = PizzaSerializer
    queryset = Pizza.objects.all()

