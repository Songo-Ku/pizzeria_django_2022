from django.contrib import admin
from django.urls import path, include
from pizzeria.views import RestaurantViewSet, ToppingViewSet, PizzaViewSet, ToppingViewSetCustom
from order_system.views import OrderViewSet, PaymentViewSet, OrderedProductsViewSet
from rest_framework import routers

# ---------------------------------------------------------
# section router
router = routers.DefaultRouter()
# pizzeria app
router.register(r'restaurants', RestaurantViewSet, basename='restaurant')
router.register(r'toppings', ToppingViewSet, basename='topping')
router.register(r'newtoppings', ToppingViewSetCustom, basename='topping')
router.register(r'pizzas', PizzaViewSet, basename='pizza')
# order system app
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'payments', PaymentViewSet, basename='payments')
router.register(r'order-products', OrderedProductsViewSet, basename='order-products')
# ---------------------------------------------------------

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('auth-custom/', include('auth_custom.urls')),  # to nie sluzy do logowania
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("api/rest-auth/", include("rest_auth.urls")),
    path("api/rest-auth/registration/", include("rest_auth.registration.urls")),
    path('api/', include(router.urls)),
]
