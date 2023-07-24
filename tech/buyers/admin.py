from django.contrib import admin

from .models import *

class ProductInCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'count', 'date', 'is_active')
    list_display_links = ('id', 'user', 'product')

class SavedAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'info', 'user')
    list_display_links = ('id', 'info', 'user')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'date')
    list_display_links = ('id', 'product', 'user')

class FavouritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user')
    list_display_links = ('id', 'product', 'user')

admin.site.register(ProductInCart, ProductInCartAdmin)
admin.site.register(SavedAddress, SavedAddressAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Favourites, FavouritesAdmin)