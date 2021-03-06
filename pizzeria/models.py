from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)
    phone_number = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('auth.User', related_name='restaurants', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'


class Pizza(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    description = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='pizzas')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f' {self.name} from {self.restaurant.name}'

    def show_toppings(self):
        return self.topping_set.all()

    def show_toppings_names(self):
        return [topping.name for topping in self.topping_set.all()]

    def show_toppings_prices(self):
        return [topping.price for topping in self.topping_set.all()]




class Topping(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    supplier = models.CharField(max_length=100)
    meals = models.ManyToManyField(Pizza)

    def __str__(self):
        return f'{self.name} w pizzach: {self.meals.all()}'




# class PizzaTopping(models.Model):
#     topping = models.ForeignKey(Topping, on_delete=models.CASCADE)
#     pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'{self.topping.name} dla pizzy:  {self.pizza.name}'


















