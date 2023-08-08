from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import datetime

from main.models import Product

class ProductInCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    date = models.DateTimeField(default=datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(hours=3))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product + ': ' + self.user + ': ' + str(self.count)

    class Meta:
        verbose_name_plural = "Product in cart"

class SavedAddress(models.Model):
    info = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.info + self.user

    class Meta:
        verbose_name_plural = "Saved addresses"

class ProductInOrder(models.Model):
    productInCart = models.ForeignKey(ProductInCart, on_delete=models.CASCADE)
    address = models.ForeignKey(SavedAddress, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.product.name + self.product.user

    class Meta:
        verbose_name_plural = "Product in order"

class Favourites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product + ': ' + self.user

    class Meta:
        verbose_name_plural = "Favourites"