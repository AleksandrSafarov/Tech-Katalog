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
        verbose_name_plural = "Products in cart"

class SavedAddress(models.Model):
    info = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.info + self.user

    class Meta:
        verbose_name_plural = "Saved addresses"

class Comment(models.Model):
    text = models.TextField()
    date = models.DateTimeField(default=datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(hours=3))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product + ': ' + self.user + ': ' + self.date

class Favourites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product + ': ' + self.user

    class Meta:
        verbose_name_plural = "Favourites"