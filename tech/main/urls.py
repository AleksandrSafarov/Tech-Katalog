from django.urls import path

from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('category/<int:category_id>/<int:sort_key>', categoryProductList, name='category'),
    path('all/<int:sort_key>', allProductsList, name='all'),
    path('product/<int:product_id>', productPage, name='product'),
    path('product/makeProductReview/<int:product_id>', makeProductReview, name='makeProductReview'),
    path('logout/', logout_user, name='logout'),
    path('product/<int:product_id>/deleteImage/<int:image_id>', deleteImage, name='deleteImage'),
    path('seller/<int:seller_id>', sellerPage, name='seller'),
    path('seller/makeSellerReview/<int:seller_id>', makeSellerReview, name='makeSellerReview'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('edituserdata/', ChangeUserData.as_view(), name='editData'),
    path('changepassword/', ChangePass.as_view(), name='changePassword'),
    path('productreviews/<int:product_id>/<int:sort_key>', productReviewsPage, name='productReviews'),
    path('sellerreviews/<int:seller_id>/<int:sort_key>', sellerReviewsPage, name='sellerReviews'),
    path('makesearch/', search, name='makeSearch'),
    path('search/<int:sort_key>', searchPage, name="search")
]