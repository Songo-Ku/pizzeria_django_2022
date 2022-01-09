# from . import views
# from rest_framework.urlpatterns import format_suffix_patterns
# from django.urls import path, include
# from rest_framework import routers
# from .views import RestaurantViewSet, ToppingViewSet, PizzaViewSet
#
#
# router = routers.DefaultRouter()
# router.register(r'restaurants', RestaurantViewSet, basename='restaurant')
# router.register(r'toppings', ToppingViewSet, basename='topping')
# router.register(r'pizzas', PizzaViewSet, basename='pizza')

# urlpatterns = format_suffix_patterns([
    # path('restaurants/', views.RestaurantViewSet.as_view({'get': 'list'}), name='restaurants-lists'),
    # path('', views.api_root),
    # path('restaurants/', views.RestaurantList.as_view(), name='restaurants-lists'),
    # path('restaurants/', views.RestaurantViewSet.as_view(), name='restaurants-lists'),
    # path('restaurants/<int:pk>/', views.RestaurantDetail.as_view(), name='restaurants-detail'),
    # path('topping/', views.ToppingList.as_view(), name='topping-lists'),
    # path('topping/<int:pk>/', views.ToppingDetail.as_view(), name='topping-detail'),

    # path('pizza/', views.PizzaList.as_view(), name='pizza-lists'),
# ])
# urlpatterns += router.urls
