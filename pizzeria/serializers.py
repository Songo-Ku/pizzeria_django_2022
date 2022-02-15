from .models import Restaurant, Pizza, Topping
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.utils import timezone


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ['pk', 'name', 'address', 'phone_number', 'pizzas', 'created', 'modified']


class RestaurantCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'phone_number']
        read_only_fields = ('pk', 'modified', 'created')


class RestaurantUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ['address', 'phone_number', 'pizzas']
        read_only_fields = ('name', 'pk', 'modified', 'created')


class PizzaSerializer(serializers.ModelSerializer):
    # local = serializers.PrimaryKeyRelatedField()
    # local = PizzeriaRestaurantSerializer()
    # local = serializers.ReadOnlyField(source='local.pk')  # to na pewno nie jest odpowiednie pole dla tego przypadku

    # owner = serializers.ReadOnlyField(source='owner.username')
    restaurant_name = serializers.ReadOnlyField(source='restaurant.name')
    modified = serializers.ReadOnlyField()

    class Meta:
        model = Pizza
        fields = ['pk', 'name', 'price', 'description', 'restaurant', 'restaurant_name', 'modified']


class ToppingSerializer(serializers.ModelSerializer):
    meals_name = serializers.ReadOnlyField(source='pizza.name')

    class Meta:
        model = Topping
        fields = ['pk', 'name', 'price', 'supplier', 'meals', 'meals_name']



















# class RestaurantSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=50)
#     address = serializers.CharField(max_length=80)
#     phone_number = serializers.IntegerField()
#     created = serializers.DateTimeField(read_only=True)
#     modified = serializers.DateTimeField(read_only=True)
#     pizzas = serializers.PrimaryKeyRelatedField(queryset=Pizza.objects.all())
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Restaurant` instance, given the validated data.
#         """
#         print('to sa validated data: ', validated_data)
#         return Restaurant.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Restaurant` instance, given the validated data.
#         """
#         instance.name = validated_data.get('name', instance.name)
#         instance.address = validated_data.get('address', instance.address)
#         instance.phone_number = validated_data.get('phone_number', instance.phone_number)
#         instance.modified = timezone.now()
#         instance.save()
#         return instance


# class PizzaSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=100)
#     price = serializers.DecimalField(max_digits=5, decimal_places=2)
#     description = serializers.CharField(max_length=80)
#     phone_number = serializers.IntegerField()
#     created = serializers.DateTimeField(read_only=True)
#     modified = serializers.DateTimeField(read_only=True)
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Restaurant` instance, given the validated data.
#         """
#         print('to sa validated data: ', validated_data)
#         return Pizza.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Restaurant` instance, given the validated data.
#         """
#         local_verification = validated_data.get('local', '')
#         local_exist_or_not = Restaurant.objects.get(pk=local_verification)
#         if len(local_exist_or_not) != 1:
#             # in case we didnt get proper local pk which do not exist then we do not want to update record
#             # we need here some exception and return HTTP error
#             return instance
#         else:
#             instance.local = validated_data.get('local', instance.local)
#             instance.name = validated_data.get('name', instance.name)
#             instance.price = validated_data.get('price', instance.price)
#             instance.description = validated_data.get('description', instance.description)
#             instance.modified = timezone.now()
#             instance.local = validated_data.get('local', instance.local)
#             instance.save()
#             return instance
#
#
# class ToppingSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     price = serializers.DecimalField(decimal_places=2, max_digits=5)
#     name = serializers.CharField(max_length=50)
#     supplier = serializers.CharField(max_length=80)
#     # pizza = serializers.PrimaryKeyRelatedField(many=True, queryset=Pizza.objects.all())
#     # user = PizzaSerializer()
#     # pizza = serializers.PrimaryKeyRelatedField(many=True, queryset=Pizza.objects.all())
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Restaurant` instance, given the validated data.
#         """
#         print('to sie wywoluje w serializer')
#         print('to sa validated data: ', validated_data)
#         return Topping.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Restaurant` instance, given the validated data.
#         """
#         print('to sie wywoluje w serializer')
#         #
#         # instance.name = validated_data.get('name', instance.name)
#         # instance.address = validated_data.get('address', instance.address)
#         # instance.phone_number = validated_data.get('phone_number', instance.phone_number)
#         # instance.modified = timezone.now()
#         # instance.save()
#         return instance
#
#

