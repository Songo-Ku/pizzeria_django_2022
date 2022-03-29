from django.db import models
from pizzeria.models import Restaurant, Topping, Pizza
from phonenumber_field.modelfields import PhoneNumberField


class ContactUser(models.Model):
    address_delivery = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    phone = PhoneNumberField(null=False, blank=False, unique=True)

    def __str__(self):
        return f' ContactData for user {self.surname} {self.name}'


class Order(models.Model):
    id_restaurant = models.IntegerField()
    contact_data = models.ForeignKey(ContactUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'zamowienie o nr. {self.pk} dla lokalu {self.get_restaurant_name_address()}'

    def get_restaurant_name_address(self):
        restaurant = Restaurant.objects.filter(pk=self.id_restaurant)
        if len(restaurant) > 0:
            return f'restauracja nr.{restaurant[0].id}  {restaurant[0].name} o adresie {restaurant[0].address}'
        else:
            return 'Not added yet - Unknown'

    def get_restaurant_name(self):
        restaurant = Restaurant.objects.filter(pk=self.id_restaurant)
        if len(restaurant) > 0:
            return f'zamowienie numer {self.pk} dla restauracji {restaurant[0].name}'
        else:
            return 'Not added yet - Unknown'

    def count_total(self):
        return sum([product.total * product.count for product in self.ordered_products.all()])


class Payment(models.Model):
    STATUS_PAYMENT = (
        ('not accepted', 'not accepted'),
        ('pending', 'pending'),
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
    pizza_name = models.CharField(max_length=40)
    count = models.IntegerField(default=1)
    total = models.DecimalField(decimal_places=2, max_digits=7)
    order = models.ForeignKey(Order, models.CASCADE, related_name='ordered_products')
    product = models.ForeignKey(Pizza, related_name='ordered_products', on_delete=models.CASCADE)

    def __str__(self):
        # return f'zamowiona pizza to {self.pizza_name} w ilosc {self.amount} za {self.amount * self.price}'
        # return f'zamowiona pizza to {self.product.name} w ilosc {self.count} za {self.count} * {self.product.price}'
        return f'zamowiona pizza to {self.product.name} '

    def set_total(self):
        # pomyslec gdzie tego uzyc zeby pole self.total bylo uzupelnione w odpowiendim czasie odpowiednim wynikiem
        return self.product.price * self.count


