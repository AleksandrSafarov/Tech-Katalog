from django.urls import path

from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('category/<int:category_id>', categoryPage, name='category'),
    path('all/', allProductsPage, name='all'),
    path('product/<int:product_id>', productPage, name='product'),
    path('logout/', logout_user, name='logout'),
    path('product/<int:product_id>/deleteImage/<int:image_id>', deleteImage, name='deleteImage'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('edituserdata/', ChangeUserData.as_view(), name='editData'),
    path('changepassword/', ChangePass.as_view(), name='changePassword'),
]