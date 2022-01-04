from .models import Restaurant, Pizza, Topping, Order, OrderedProducts, Payment
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.utils import timezone


class RestaurantSerializer(serializers.Serializer):
    # pk = serializers.Field()
    name = serializers.CharField(max_length=50)
    address = serializers.CharField(max_length=80)
    phone_number = serializers.IntegerField()
    # created = serializers.DateTimeField()
    modified = serializers.DateTimeField(read_only=True)


    def create(self, validated_data):
        """
        Create and return a new `Restaurant` instance, given the validated data.
        """
        print('to sa validated data: ', validated_data)
        return Restaurant.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Restaurant` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.modified = timezone.now()
        instance.save()
        return instance