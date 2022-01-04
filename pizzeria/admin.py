from django.contrib import admin
from .models import Restaurant, Pizza, Topping, Order, OrderedProducts, Payment

admin.site.register(Restaurant)
admin.site.register(Topping)
admin.site.register(Order)
admin.site.register(OrderedProducts)
admin.site.register(Payment)


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('name', 'local')
