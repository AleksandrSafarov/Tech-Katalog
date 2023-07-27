from django.urls import path

from .views import *

urlpatterns = [
    path('seller/<int:seller_id>', sellerPage, name='seller'),
    path('createseller', CreateSeller.as_view(), name='createSeller'),
]