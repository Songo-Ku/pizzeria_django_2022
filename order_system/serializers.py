from pizzeria.models import Restaurant, Pizza, Topping
from pizzeria.serializers import PizzaSerializer
from .models import Order, OrderedProducts, Payment, ContactUser
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.utils import timezone


class ContactUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUser
        fields = ['address_delivery', 'name', 'surname', 'phone']


class ContactUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUser
        fields = ['id', 'address_delivery', 'name', 'surname', 'phone']


class OrderSerializer(serializers.ModelSerializer):
    payment_status = serializers.ReadOnlyField(source='payment.status')
    # ordered_products_names = serializers.ReadOnlyField(source='ordered_products.pizza_name', )
    # ordered_products = OrderedProductsSerializer(read_only=True)
    # ordered_products = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    # ordered_products = serializers.PrimaryKeyRelatedField(queryset=OrderedProducts.objects.all())
    #  'ordered_products'
    ordered_products = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='order-product-detail'
    )

    class Meta:
        model = Order
        fields = ['pk', 'restaurant', 'payment_status', 'contact_user', 'ordered_products']   # , 'ordered_products_names' , #ordered_products


class PaymentSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.ReadOnlyField(source='order.restaurant.name')
    restaurant_id = serializers.ReadOnlyField(source='order.restaurant.pk')

    class Meta:
        model = Payment
        fields = ['pk', 'order', 'status', 'restaurant_name', 'restaurant_id']


class OrderedProductsSerializer(serializers.ModelSerializer):
    # meals_name = serializers.ReadOnlyField(source='pizza.name')
    # order_name = serializers.ReadOnlyField(source='order.name')  # to nie działa
    # serializers.StringRelatedField(many=True) __str__ wyswietli takie info
    order_name = serializers.ReadOnlyField(source='order.restaurant.name')
    # product = serializers.PrimaryKeyRelatedField(queryset=Pizza.objects.all())
    product = PizzaSerializer(read_only=True)

    class Meta:
        model = OrderedProducts
        fields = ['pk', 'count', 'order', 'order_name', 'product']
        
    def create(self, validated_data):
        # recalcualted_price = sum([pizza.price for pizza in validated_data['product']])
        # validated_data['total'] = recalcualted_price
        return super(OrderedProductsSerializer, self).create(validated_data)


class OrderedProductsCreateSerializer(serializers.ModelSerializer):
    order_name = serializers.ReadOnlyField(source='order.get_restaurant_name')
    product = serializers.PrimaryKeyRelatedField(queryset=Pizza.objects.all())

    class Meta:
        model = OrderedProducts
        fields = ['pk', 'count', 'order', 'order_name', 'product', 'pizza_name']

    def create(self, validated_data):
        print('to jest validated data from create productsserializers \n', validated_data)
        validated_data['total'] = 0
        return super(OrderedProductsCreateSerializer, self).create(validated_data)































# class OrderStrSerializer(serializers.ModelSerializer):
#     myself = serializers.StringRelatedField()
#
#     class Meta:
#         model = Order
#         fields = ['pk', 'total', 'id_restaurant', 'payment_status', 'myself']





