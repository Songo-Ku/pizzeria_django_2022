from .models import Order, OrderedProducts, Payment
from .serializers import OrderSerializer, PaymentSerializer, OrderedProductsSerializer
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
        # if self.action == 'create' or self.action == 'update':
        #     return OrderedProductsCreateSerializer
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


    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #
    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}
    #
    #     return Response(serializer.data)
    #
    # def perform_update(self, serializer):
    #     serializer.save()



