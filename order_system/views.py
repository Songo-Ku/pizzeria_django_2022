from .models import Order, OrderedProducts, Payment
from .serializers import OrderSerializer, PaymentSerializer, OrderedProductsSerializer
from rest_framework import viewsets


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


