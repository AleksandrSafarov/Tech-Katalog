from django.contrib import admin

from .models import *

class SellerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'is_sertificated')
    list_display_links = ('id', 'name', 'user')

class SellerRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'value', 'seller', 'user')
    list_display_links = ('id', 'value', 'seller')

admin.site.register(Seller, SellerAdmin)
admin.site.register(SellerRating, SellerRatingAdmin)