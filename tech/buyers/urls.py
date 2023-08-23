from django.urls import path

from .views import *

urlpatterns = [
    path('favorite/<int:product_id>', favoriteFunc, name='favorite'),
    path('addtocart/<int:product_id>', addToCart, name='addToCart'),
    path('plus/<int:product_id>', plusProductInCart, name='plusProductInCart'),
    path('minus/<int:product_id>', minusProductInCart, name='minusProductInCart')
]