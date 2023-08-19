from django.shortcuts import render

from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import redirect
from django.urls.base import reverse_lazy
from django.views.generic import *
from django.http import Http404

from .models import *

def favoriteFunc(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        product = Product.objects.get(id=product_id)
    except:
        raise Http404
    favorite = Favorites.objects.filter(product=product, user=request.user)
    if len(favorite) == 0:
        newFavorite = Favorites(product=product, user=request.user)
        newFavorite.save()
    else:
        favorite[0].delete()
    print(next)
    return redirect('product', product_id)