from django.urls import path

from .views import *

urlpatterns = [
    path('seller/<int:seller_id>', sellerPage, name='seller'),
    path('createseller/', CreateSeller.as_view(), name='createSeller'),
    path('sellerArea/', SellerArea.as_view(), name='sellerArea'),
    path('management/', ProductManagement.as_view(), name='productManagement'),
    path('newStock/<int:product_id>', changeStockPage, name='newStock'),
    path('newStock/changeStock/<int:product_id>', changeStock, name='changeStock'),
    path('newPrice/<int:product_id>', changePricePage, name='newPrice'),
    path('newPrice/changePrice/<int:product_id>', changePrice, name='changePrice'),
]