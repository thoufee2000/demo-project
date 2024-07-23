from django.db import models
from shop.models import Product
from django.contrib.auth.models import User


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    def subtotal(self):
        return self.quantity * self.product.price


class Order_table(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    no_of_items = models.IntegerField()
    phone = models.CharField(max_length=12)
    address = models.TextField()
    pin = models.CharField(max_length=30)
    ordered_date = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=100, blank=True)
    payment_status = models.CharField(default="pending", max_length=30)
    delivery_status = models.CharField(default="pending", max_length=30)

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    name = models.CharField(max_length=50)
    amount = models.CharField(max_length=50)
    order_id = models.CharField(max_length=50, blank=True)
    razorpay_payment_id = models.CharField(max_length=50, blank=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.name
