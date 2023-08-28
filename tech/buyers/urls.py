from django.urls import path

from .views import *

urlpatterns = [
    path('addtofavorite/<int:product_id>', favoriteFunc, name='addToFavorite'),
    path('addtocart/<int:product_id>', addToCart, name='addToCart'),
    path('plus/<int:product_id>', plusProductInCart, name='plusProductInCart'),
    path('minus/<int:product_id>', minusProductInCart, name='minusProductInCart'),
    path('delete/<int:product_id>', deleteProductInCart, name='deleteProductInCart'),
    path('favorite/<int:sort_key>', favoritePage, name='favorite'),
    path('cart/', cartPage, name='cart'),
    path('cart/makeorder', makeOrder, name='makeOrder')
]