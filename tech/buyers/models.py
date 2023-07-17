from django.db import models
from django.contrib.auth.models import User
from main.models import Product

class ProductInCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

class SavedAddress(models.Model):
    info = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)