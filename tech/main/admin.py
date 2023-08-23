from django.contrib import admin

from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'plural_name')
    list_display_links = ('id', 'name', 'plural_name')
    search_fields = ('name', 'plural_name')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'stock', 'price', 'seller', 'category')
    list_display_links = ('id', 'name')

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product')
    list_display_links = ('id', 'product')

class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'value', 'product', 'finish_date')
    list_display_links = ('id', 'value', 'product')

class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'value', 'product', 'user')
    list_display_links = ('id', 'value', 'product')

class RAMValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'value')
    list_display_links = ('id', 'value')

class RAMAdmin(admin.ModelAdmin):
    list_display = ('id', 'RAM_value', 'product')
    list_display_links = ('id', 'RAM_value')

class StorageValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'value')
    list_display_links = ('id', 'value')

class StorageAdmin(admin.ModelAdmin):
    list_display = ('id', 'storage_value', 'product')
    list_display_links = ('id', 'storage_value')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(ProductRating, ProductRatingAdmin)
admin.site.register(RAMValue, RAMValueAdmin)
admin.site.register(RAM, RAMAdmin)
admin.site.register(StorageValue, StorageValueAdmin)
admin.site.register(Storage, StorageAdmin)