from django.contrib import admin

from .models import *

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Discount)
admin.site.register(ProductRating)
admin.site.register(SellerRating)