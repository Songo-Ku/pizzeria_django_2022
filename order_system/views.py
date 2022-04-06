from .models import Order, OrderedProducts, Payment, ContactUser
from .serializers import OrderSerializer, PaymentSerializer, OrderedProductsSerializer, OrderedProductsCreateSerializer, \
    ContactUserSerializer, ContactUserCreateSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response


class ContactUserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = ContactUserSerializer
    queryset = ContactUser.objects.all()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return ContactUserCreateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        print(serializer.validated_data)
        serializer.validated_data['created_by'] = self.request.user
        super().perform_create(serializer)


class OrderViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class PaymentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class OrderedProductsViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = OrderedProductsSerializer
    queryset = OrderedProducts.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return OrderedProductsCreateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print('request data to: \n:', request.data)
        print('serializer to: \n:', serializer)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()
        print('ten serializer został zasave-wowany \n', serializer.data)

