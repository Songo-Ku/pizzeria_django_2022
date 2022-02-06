from django.shortcuts import render
# from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import mixins, generics, renderers
from .models import Restaurant, Topping, Pizza
from .serializers import \
    RestaurantSerializer, ToppingSerializer, PizzaSerializer, RestaurantUpdateSerializer, RestaurantCreateSerializer
from rest_framework import viewsets


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return RestaurantCreateSerializer
        elif self.action == 'update':
            return RestaurantUpdateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print('request data to: \n:', request.data)

        serializer.is_valid(raise_exception=True)
        print('serializer to: \n:', serializer)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()
        print('serializer.data to: \n:', serializer.data)
        print('ten serializer bedzie save-wowany \n', serializer.data)


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

