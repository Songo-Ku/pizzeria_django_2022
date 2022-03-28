from .models import Order, OrderedProducts, Payment
from .serializers import OrderSerializer, PaymentSerializer, OrderedProductsSerializer, OrderedProductsCreateSerializer
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response


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


class OrderedProductsViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = OrderedProductsSerializer
    queryset = OrderedProducts.objects.all()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return OrderedProductsCreateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print('request data to: \n:', request.data)
        print('serializer to: \n:', serializer)
        print('serializer.data to: \n:', serializer.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()
        print('ten serializer bedzie save-wowany \n', serializer.data)


