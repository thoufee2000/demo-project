from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

class Category(models.Model):
    image=models.ImageField(upload_to='media/image',blank=True,null=True)
    title=models.CharField(max_length=20)
    desc=models.TextField()

    def __str__(self):
        return self.title

class Product(models.Model):
    name=models.CharField(max_length=20)
    desc=models.TextField()
    image=models.ImageField(upload_to='media/products',blank=True,null=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# class UserDetails(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.user.username

