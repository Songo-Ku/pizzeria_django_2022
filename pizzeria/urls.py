from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include


urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('restaurants/', views.RestaurantList.as_view(), name='restaurants-lists'),
    path('restaurants/<int:pk>/', views.RestaurantDetail.as_view(), name='restaurants-detail'),
    path('topping/', views.ToppingList.as_view(), name='topping-lists'),
    path('pizza/', views.PizzaList.as_view(), name='pizza-lists'),
])
