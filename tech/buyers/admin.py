from django.contrib import admin

from .models import *

class ProductInCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'count', 'date', 'is_active')
    list_display_links = ('id', 'user', 'product')

class SavedAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'info', 'user')
    list_display_links = ('id', 'info', 'user')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date')
    list_display_links = ('id', 'date')

class FavouritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user')
    list_display_links = ('id', 'product', 'user')

admin.site.register(ProductInCart, ProductInCartAdmin)
admin.site.register(SavedAddress, SavedAddressAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Favorites, FavouritesAdmin)