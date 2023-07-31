from django.urls import path

from .views import *

urlpatterns = [
    path('seller/<int:seller_id>', sellerPage, name='seller'),
    path('createseller/', CreateSeller.as_view(), name='createSeller'),
    path('createproduct/', CreateProduct.as_view(), name='createProduct'),
    path('sellerarea/', SellerArea.as_view(), name='sellerArea'),
    path('management/', ProductManagement.as_view(), name='productManagement'),
    path('newstock/<int:product_id>', changeStockPage, name='newStock'),
    path('newstock/changeStock/<int:product_id>', changeStock, name='changeStock'),
    path('newprice/<int:product_id>', changePricePage, name='newPrice'),
    path('newprice/changePrice/<int:product_id>', changePrice, name='changePrice'),
]