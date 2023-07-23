from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

import datetime

from sellers.models import Seller

class Category(models.Model):
    name = models.CharField(max_length=50)
    plural_name = models.CharField(max_length=50, default="")

class Product(models.Model):
    name = models.CharField(max_length=200)
    stock = models.PositiveIntegerField(default=1)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100_000_000_000)])
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    main_image = models.ImageField(upload_to='images/products/')

class ProductImage(models.Model):
    image = models.ImageField(upload_to='images/products/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Discount(models.Model):
    value = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(99)])
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    finish_date = models.DateTimeField(default=datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(hours=3))

class ProductRating(models.Model):
    score = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class SellerRating(models.Model):
    score = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

class Popularity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    finish_date = models.DateTimeField(default=datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(hours=3))