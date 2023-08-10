from django.urls import path

from .views import *

urlpatterns = [
    path('seller/<int:seller_id>', sellerPage, name='seller'),
    path('createseller/', CreateSeller.as_view(), name='createSeller'),
    path('createproduct/', CreateProduct.as_view(), name='createProduct'),
    path('sellerarea/', SellerArea.as_view(), name='sellerArea'),
    path('management/', ProductManagement.as_view(), name='productManagement'),
    path('newdata/<int:product_id>', changeDataPage, name='newData'),
    path('newdata/changedata/<int:product_id>', changeData, name='changeData'),
    path('addproductimage/<int:product_id>', addProductImage, name='addProductImage'),
    path('makediscount/<int:product_id>', makeDiscountPage, name='makeDiscountPage'),
    path('makediscount/discount/<int:product_id>', makeDiscount, name='makeDiscount'),
]