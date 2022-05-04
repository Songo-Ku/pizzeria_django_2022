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
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    contact_user = models.ForeignKey(ContactUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'zamowienie o nr. {self.pk} dla lokalu {self.restaurant.name} o id: {self.restaurant.pk}'

    def count_total(self):
        return sum([product.price * product.count for product in self.ordered_products.all()])


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

    def get_status_pending(self):
        self.status = 'pending'
        self.save()

    def get_payment_confirm(self):
        self.status = 'accepted'
        self.save()


class OrderedProducts(models.Model):
    count = models.IntegerField(default=1)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    order = models.ForeignKey(Order, models.CASCADE, related_name='ordered_products')
    product = models.ForeignKey(Pizza, related_name='ordered_products', on_delete=models.CASCADE)

    def __str__(self):
        return f'zamowiona pizza to {self.product.name} '

    def total_cost_for_ordered_product(self):
        return self.product.price * self.count


