from django.db import models
from pizzeria.models import Restaurant, Topping, Pizza


class Order(models.Model):
    # tu potrzebne jest jeszcze polaczenie do ktorej pizzeri nalezy to zamowienie
    total = models.DecimalField(decimal_places=2, max_digits=7)
    id_restaurant = models.IntegerField()  # moze to powinno mieć połączenie z dana restauracja manytomany???

    def __str__(self):
        return f'zamowienie o nr. {self.pk} dla lokalu {self.get_restaurant_name_address()}'

    def get_restaurant_name_address(self):
        restaurant = Restaurant.objects.filter(pk=self.id_restaurant)
        if len(restaurant) > 0:
            return f'restauracja {restaurant[0].name} o adresie {restaurant[0].address}'
        else:
            return 'Not added yet - Unknown'

    def get_restaurant_name(self):
        restaurant = Restaurant.objects.filter(pk=self.id_restaurant)
        if len(restaurant) > 0:
            return f'restaurant name: {restaurant[0].name}'
        else:
            return 'Not added yet - Unknown'

    def set_total(self, total):
        calculated_total = self.orderedproducts_set.all()
        # -----------------------------------
        # -----------------------------------
        # tutaj  zwrocic odpowiednia kwote za kazdym razem i napisac
        self.total = total


class Payment(models.Model):
    STATUS_PAYMENT = (
        ('not accepted', 'not accepted'),
        ('accepted', 'accepted'),
    )
    status = models.CharField(max_length=100, choices=STATUS_PAYMENT, default='not accepted')
    order = models.OneToOneField(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.status}'

    def get_payment_confirm(self):
        self.status = 'accepted'
        self.save()


class OrderedProducts(models.Model):
    pizza_name = models.CharField(max_length=20)  # dlaczego tutaj nie moze byc ManyToManyField
    amount = models.IntegerField(default=1)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    order = models.ForeignKey(Order, models.CASCADE, related_name='ordered_products')

    def __str__(self):
        return f'zamowiona pizza to {self.pizza_name} w ilosc {self.amount} za {self.amount * self.price}'


