from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response


# class RestaurantViewSet(viewsets.ViewSet):
#     """
#     A simple ViewSet for listing or retrieving users.
#     """
#     def list(self, request):
#         queryset = Restaurant.objects.all()
#         serializer = RestaurantSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = Restaurant.objects.all()
#         restaurant = get_object_or_404(queryset, pk=pk)
#         serializer = RestaurantSerializer(restaurant)
#         return Response(serializer.data)


# class RestaurantList(mixins.ListModelMixin,
#                      mixins.CreateModelMixin,
#                      generics.GenericAPIView):
#     queryset = Restaurant.objects.all()
#     serializer_class = RestaurantSerializer
#     # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#     def perform_create(self, serializer):
#         serializer.save()


# class RestaurantDetail(mixins.RetrieveModelMixin,
#                         mixins.UpdateModelMixin,
#                         mixins.DestroyModelMixin,
#                         generics.GenericAPIView):
#     queryset = Restaurant.objects.all()
#     serializer_class = RestaurantSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # def get(self, request, *args, **kwargs):
    #     return self.retrieve(request, *args, **kwargs)
    #
    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)
    #
    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)


# class ToppingList(mixins.ListModelMixin,
#                      mixins.CreateModelMixin,
#                      generics.GenericAPIView):
#     queryset = Topping.objects.all()
#     serializer_class = ToppingSerializer
#     # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def get(self, request, *args, **kwargs):
#         print('to sie wywoluje w widoku dla get')
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         print('to sie wywoluje w widoku dla post')
#         return self.create(request, *args, **kwargs)
#
#     def create(self, request, *args, **kwargs):
#         print('to sie wywoluje w widoku dla create')
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#
#     def perform_create(self, serializer):
#         print('to sie wywoluje w widoku dla perform create')
#         serializer.save()
#
#
# class PizzaList(mixins.ListModelMixin,
#                      mixins.CreateModelMixin,
#                      generics.GenericAPIView):
#     queryset = Pizza.objects.all()
#     serializer_class = PizzaSerializer
#     # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#
#     def perform_create(self, serializer):
#         serializer.save()
#
#
# class ToppingDetail(mixins.RetrieveModelMixin,
#                         mixins.UpdateModelMixin,
#                         mixins.DestroyModelMixin,
#                         generics.GenericAPIView):
#     queryset = Topping.objects.all()
#     serializer_class = ToppingSerializer
#     # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         'restaurants': reverse('restaurants-lists', request=request, format=format),
#     })