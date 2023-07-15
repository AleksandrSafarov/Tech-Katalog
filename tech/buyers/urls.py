from django.urls import path

from .views import *

urlpatterns = [
    path('logout/', logout_user, name='buyerLogout'),
    path('signup/', BuyerSignUp.as_view(), name='buyerSignup'),
    path('login/', BuyerLogin.as_view(), name='buyerLogin'),
    path('edituserdata/', BuyerChangeUserData.as_view(), name='buyerEditData'),
    path('changepassword/', BuyerChangePass.as_view(), name='buyerChangePassword'),
    #path('personalArea/', PersonalArea.as_view(), name='personalArea')
]