from django.contrib import admin
from django.urls import path, include
from pizzeria import urls as pizza_urls

from rest_framework import routers


# router = routers.DefaultRouter()
# router = routers.SimpleRouter()
# router.register(r'/xx', api_root)
# router.register(r'', api_root)
# router.register(r'restaurant', RestaurantList)

# router.register(r'accounts', AccountViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('pizzeria.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(pizza_urls)),
    # path('router/', include(router)),
]
# urlpatterns += router.urls
