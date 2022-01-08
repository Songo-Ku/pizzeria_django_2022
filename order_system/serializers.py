from pizzeria.models import Restaurant, Pizza, Topping
from .models import Order, OrderedProducts, Payment

from django.contrib.auth.models import User, Group
from rest_framework import serializers


# class RestaurantSerializer(serializers.ModelSerializer):
#     pizzas = serializers.PrimaryKeyRelatedField(queryset=Pizza.objects.all(), )
#
#     class Meta:
#         model = Restaurant
#         fields = ['pk', 'name', 'address', 'phone_number', 'pizzas', 'created', 'modified']
#
#
# class PizzaSerializer(serializers.ModelSerializer):
#     # local = serializers.PrimaryKeyRelatedField()
#     # local = PizzeriaRestaurantSerializer()
#     # local = serializers.ReadOnlyField(source='local.pk')  # to na pewno nie jest odpowiednie pole dla tego przypadku
#
#     # owner = serializers.ReadOnlyField(source='owner.username')
#     restaurant_name = serializers.ReadOnlyField(source='restaurant.name')
#     modified = serializers.ReadOnlyField()
#
#     class Meta:
#         model = Pizza
#         fields = ['pk', 'name', 'price', 'description', 'restaurant', 'restaurant_name', 'modified']
#
#
# class ToppingSerializer(serializers.ModelSerializer):
#     # local = serializers.PrimaryKeyRelatedField()
#     # local = PizzeriaRestaurantSerializer()
#     # local = serializers.ReadOnlyField(source='local.pk')  # to na pewno nie jest odpowiednie pole dla tego przypadku
#
#     # owner = serializers.ReadOnlyField(source='owner.username')
#     restaurant_name = serializers.ReadOnlyField(source='restaurant.name')
#     modified = serializers.ReadOnlyField()
#
#     class Meta:
#         model = Topping
#         fields = ['pk', 'name', 'price', 'description', 'restaurant', 'restaurant_name', 'modified']

