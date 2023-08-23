from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

import datetime

from sellers.models import Seller
from buyers.models import *

class Category(models.Model):
    name = models.CharField(max_length=50)
    plural_name = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    name = models.CharField(max_length=200)
    stock = models.PositiveIntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(100_000_000)])
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100_000_000_000)])
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    main_image = models.ImageField(upload_to='images/products/')

    def __str__(self):
        return self.name
    
    def getStock(self):
        if self.stock:
            return self.stock
        return 'Нет в наличии'
    
    def getAvgProductRating(self):
        reviews = list(ProductRating.objects.filter(product=self))
        if len(reviews) == 0:
            return 0
        avgRating = round(sum(r.value for r in reviews) / len(reviews), 2)
        if avgRating % 1 == 0:
            return int(avgRating)
        return avgRating
    
    def getProductRatingCount(self):
        return len(list(ProductRating.objects.filter(product=self)))
    
    def hasDiscount(self):
        try:
            discount = Discount.objects.get(product=self)
        except:
            return False
        return True
    
    def getDiscountValue(self):
        try:
            discount = Discount.objects.get(product=self)
        except:
            return 0
        return discount.value
    
    def getPriceWithDiscount(self):
        try:
            discount = Discount.objects.get(product=self)
        except:
            return self.price
        priceWithDiscount = int(self.price * (1 - (discount.value / 100)))
        if priceWithDiscount == 0:
            return 1
        return priceWithDiscount

class ProductImage(models.Model):
    image = models.ImageField(upload_to='images/products/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name

class Discount(models.Model):
    value = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(99)])
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    finish_date = models.DateTimeField()

    def __str__(self):
        return self.product.name + '; ' + str(self.value)
    
    def getdate(self):
        return str(self.finish_date.day).zfill(2)+'.'+str(self.finish_date.month).zfill(2)+'.'+str(self.finish_date.year)

class ProductRating(models.Model):
    value = models.IntegerField(default=1)
    plus = models.TextField(null=True)
    minus = models.TextField(null=True)
    text = models.TextField(null=True)
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name + ': ' + str(self.value)
    
    def getdate(self):
        return str(self.date.day).zfill(2)+'.'+str(self.date.month).zfill(2)+'.'+str(self.date.year)

class Popularity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    finish_date = models.DateTimeField()

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name_plural = "Popularity"

class RAMValue(models.Model):
    value = models.IntegerField()

    def __str__(self):
        return str(self.value)
    
    class Meta:
        verbose_name_plural = "RAM values"

class RAM(models.Model):
    RAM_value = models.ForeignKey(RAMValue, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.RAM_value) + ' ' + self.product
    
    class Meta:
        verbose_name_plural = "RAM"

class StorageValue(models.Model):
    value = models.IntegerField()

    def __str__(self):
        return str(self.value)
    
    class Meta:
        verbose_name_plural = "Storage values"

class Storage(models.Model):
    storage_value = models.ForeignKey(StorageValue, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.storage_value) + ' ' + self.product
    
    class Meta:
        verbose_name_plural = "Storage"