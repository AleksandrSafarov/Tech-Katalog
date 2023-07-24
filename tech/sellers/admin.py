from django.contrib import admin

from .models import *

class SellerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'is_sertificated')
    list_display_links = ('id', 'name', 'user')

admin.site.register(Seller, SellerAdmin)