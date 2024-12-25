from django.db import models
from django.contrib.auth.models import User
from product.models import Product

class OrderStatus(models.TextChoices):
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'

class PaymentStatus(models.TextChoices):
    PAID = 'PAID'
    UNPAID = 'UNPAID'

class PaymentMode(models.TextChoices):
    COD = 'COD'  # Cash on Delivery
    CARD = 'CARD'

class Order(models.Model):
    street = models.CharField(max_length=100, default="", blank=False)
    city = models.CharField(max_length=100, default="", blank=False)
    state = models.CharField(max_length=100, default="", blank=False)
    zip_code = models.CharField(max_length=100, default="", blank=False)
    phone_no = models.CharField(max_length=100, default="", blank=False)
    country = models.CharField(max_length=100, default="", blank=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    payment_status = models.CharField(
        max_length=100,
        choices=PaymentStatus.choices,
        default=PaymentStatus.UNPAID
    )
    status = models.CharField(
        max_length=100,
        choices=OrderStatus.choices,
        default=OrderStatus.PROCESSING
    )
    payment_mode = models.CharField(
        max_length=100,
        choices=PaymentMode.choices,
        default=PaymentMode.COD
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name="orderitems")
    name = models.CharField(max_length=100, default="", blank=False)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)

    def __str__(self):
        return str(self.name)
