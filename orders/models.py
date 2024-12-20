from django.db import models
from shop.models import Product
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon

class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='orders',
        blank=True,
        null = True,
        on_delete=models.CASCADE)

    email = models.EmailField()
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    street = models.CharField(max_length=150)
    house_number = models.CharField(max_length=10, verbose_name="House number")
    apartment_number = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Apartment number"
    )  # Может быть пустым для частных домов

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=250, blank=True)
    coupon = models.ForeignKey(
        Coupon,
        related_name='orders',
        null=True,
        blank=True,
        on_delete=models.SET_NULL)

    discount = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ])

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()

    def get_yookassa_url(self):
        if not self.payment_id:
            return ''
        else:
            return f'https://yookassa.ru/my/payments?search={self.payment_id}'

    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return int(total_cost * (self.discount / 100))
        return 0

class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity