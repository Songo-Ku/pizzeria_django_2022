from pizzeria.models import Restaurant, Pizza, Topping
from pizzeria.serializers import PizzaSerializer
from .models import Order, OrderedProducts, Payment
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.utils import timezone


class OrderSerializer(serializers.ModelSerializer):
    payment_status = serializers.ReadOnlyField(source='payment.status')
    # ordered_products_names = serializers.ReadOnlyField(source='ordered_products.pizza_name', )
    # nie wiem jak uzyskac liste z nazwami pizz z tabeli ordered_products, souirce w tym przypadku nie dziala.

    class Meta:
        model = Order
        fields = ['pk', 'total', 'id_restaurant', 'payment_status', 'ordered_products']  # , 'ordered_products_names'


class PaymentSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.ReadOnlyField(source='order.get_restaurant_name')
    restaurant_id = serializers.ReadOnlyField(source='order.id_restaurant')

    class Meta:
        model = Payment
        fields = ['pk', 'order', 'status', 'restaurant_name', 'restaurant_id']


class OrderedProductsSerializer(serializers.ModelSerializer):
    # meals_name = serializers.ReadOnlyField(source='pizza.name')
    order_name = serializers.ReadOnlyField(source='order.name')
    # serializowany_produkt = PizzaSerializer()  opracować to

    class Meta:
        model = OrderedProducts
        fields = ['pk', 'count', 'order', 'order_name', 'product']  #, 'serializowany_produkt'




