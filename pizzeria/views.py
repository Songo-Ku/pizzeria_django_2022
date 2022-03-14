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

    # def create(self, request, *args, **kwargs):
    #     data = request.data
    #     data['owner'] = request.user
    #     serializer = self.get_serializer(data=data)
    #     # print('request data to: \n:', request.data)
    #
    #     serializer.is_valid(raise_exception=True)
    #     # print('serializer to: \n:', serializer)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #
    # def perform_create(self, serializer):
    #     print(self.request.user, '\n jest w perform create')
    #     serializer.save(owner=self.request.user)  # to musi byc w przeciwnym razie nie bedzie dobrze przekazany owner
    #     restaurants = Restaurant.objects.all()
    #     print('to sa restauracje po perform create', restaurants)


    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
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
        if request.data:
            print(request.data, '\n reuqest data')
            print(request.data.get("vote"))
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
            print(request.data, '\n reuqest data')
            print(request.data.get("vote"))
        if request.data:
            print(request.data, '\n reuqest data')
            print(request.data.get("choice"))
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
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = PizzaSerializer
    queryset = Pizza.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


    # def get_permissions(self):
    #     # Your logic should be all here
    #     if self.request.method == 'GET':
    #         self.permission_classes = [DummyPermission, ]
    #     else:
    #         self.permission_classes = [IsAuthenticated, ]
    #
    #     return super(UsersViewSet, self).get_permissions()
#
#     def update(self, request, *args, **kwargs):
#         self.methods=('put',)
#         self.permission_classes = (permissions.CustomPermissions,)
#         return super(self.__class__, self).update(request, *args, **kwargs)


