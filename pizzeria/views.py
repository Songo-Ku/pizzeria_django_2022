from django.shortcuts import render
# from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import mixins, generics, renderers
from .models import Restaurant, Topping, Pizza
from .serializers import \
    RestaurantSerializer, ToppingSerializer, PizzaSerializer, RestaurantUpdateSerializer, RestaurantCreateSerializer, \
    PizzaCreateSerializer
from rest_framework import viewsets
from rest_framework import permissions

# create mixins from modelviewset
from rest_framework.settings import api_settings



from django.contrib.auth.models import User


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'create':
            return RestaurantCreateSerializer
        elif self.action == 'update':
            return RestaurantUpdateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = []
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class ToppingViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = ToppingSerializer
    queryset = Topping.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ToppingViewSetCustom(viewsets.ModelViewSet):
    serializer_class = ToppingSerializer
    queryset = Topping.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.data:
            print(request.data, '\nreuqest data')
            print(request.data.get("choice", 'nie ma choice'))
            print(request.data.get("vote", 'nie ma vote'))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class PizzaViewSet(viewsets.ModelViewSet):
    serializer_class = PizzaSerializer
    queryset = Pizza.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return PizzaCreateSerializer
        # elif self.action == 'update':
        #     return PizzaUpdateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = []
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]




