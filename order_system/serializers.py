from pizzeria.models import Restaurant, Pizza, Topping
from pizzeria.serializers import PizzaSerializer
from .models import Order, OrderedProducts, Payment, ContactUser
from rest_framework import serializers


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
    ordered_products = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='order-product-detail'
    )

    class Meta:
        model = Order
        fields = ['pk', 'restaurant', 'payment_status', 'contact_user', 'ordered_products']


class PaymentSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.ReadOnlyField(source='order.restaurant.name')
    restaurant_id = serializers.ReadOnlyField(source='order.restaurant.pk')

    class Meta:
        model = Payment
        fields = ['pk', 'order', 'status', 'restaurant_name', 'restaurant_id']
        read_only_fields = ['pk']


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['pk', 'order', 'status']
        read_only_fields = ['pk', 'status']

    def create(self, validated_data):
        return super(PaymentCreateSerializer, self).create(validated_data)


class PaymentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['pk', 'order', 'status']
        read_only_fields = ['pk']


class OrderedProductsSerializer(serializers.ModelSerializer):
    # meals_name = serializers.ReadOnlyField(source='pizza.name')
    # order_name = serializers.ReadOnlyField(source='order.name')  # to nie działa
    # serializers.StringRelatedField(many=True) __str__ wyswietli takie info
    restaurant_name = serializers.ReadOnlyField(source='order.restaurant.name')
    # product = serializers.PrimaryKeyRelatedField(queryset=Pizza.objects.all())
    product = PizzaSerializer(read_only=True)
    total = serializers.ReadOnlyField(source='total_cost_for_ordered_product')

    class Meta:
        model = OrderedProducts
        fields = ['pk', 'count', 'order', 'restaurant_name', 'product', 'price', 'total']
        read_only_fields = ['pk']


class OrderedProductsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedProducts
        fields = ['pk', 'count', 'order', 'product', 'price']
        read_only_fields = ['pk']


class OrderedProductsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedProducts
        fields = ['pk', 'count', 'order', 'product', 'price']
        read_only_fields = ['pk', 'price']

    def create(self, validated_data):
        if validated_data['product']:
            validated_data['price'] = validated_data['product'].price
        else:
            validated_data['price'] = 0
        return super(OrderedProductsCreateSerializer, self).create(validated_data)


class OrderedProductsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedProducts
        fields = ['pk', 'count', 'order', 'product', 'price']
        read_only_fields = ['pk', 'price']






























# class OrderStrSerializer(serializers.ModelSerializer):
#     myself = serializers.StringRelatedField()
#
#     class Meta:
#         model = Order
#         fields = ['pk', 'total', 'id_restaurant', 'payment_status', 'myself']





