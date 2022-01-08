from django.contrib import admin
from .models import Restaurant, Pizza, Topping


admin.site.register(Restaurant)
admin.site.register(Pizza)
admin.site.register(Topping)




# @admin.register(Pizza)
# class PizzaAdmin(admin.ModelAdmin):
#     list_display = ('name', 'local')
