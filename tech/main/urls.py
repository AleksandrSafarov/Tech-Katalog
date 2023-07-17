from django.urls import path

from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('logout/', logout_user, name='logout'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('edituserdata/', ChangeUserData.as_view(), name='editData'),
    path('changepassword/', ChangePass.as_view(), name='changePassword'),
    #path('personalArea/', PersonalArea.as_view(), name='personalArea')
]