from django.urls import path

from .views import *

urlpatterns = [
    path('favorite/<int:product_id>', favoriteFunc, name='favorite')
]