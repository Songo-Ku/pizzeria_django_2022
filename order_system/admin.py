from django.contrib import admin
from .models import Order, OrderedProducts, Payment, ContactUser
# Register your models here.


admin.site.register(Order)
admin.site.register(OrderedProducts)
admin.site.register(Payment)
admin.site.register(ContactUser)

