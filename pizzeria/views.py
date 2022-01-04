from django.shortcuts import render
# from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import mixins, generics, renderers
from .models import Restaurant
from .serializers import RestaurantSerializer
from rest_framework import permissions


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'restaurants': reverse('restaurants-lists', request=request, format=format),
    })


class RestaurantList(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()


class RestaurantDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

