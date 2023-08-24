from django.shortcuts import render

from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import redirect
from django.urls.base import reverse_lazy, reverse
from django.views.generic import *
from django.http import Http404

from .models import *
from .utils import *

import datetime

def favoriteFunc(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        product = Product.objects.get(id=product_id)
    except:
        raise Http404
    
    favorite = list(Favorites.objects.filter(product=product, user=request.user))
    if len(favorite) == 0:
        newFavorite = Favorites(product=product, user=request.user)
        newFavorite.save()
    else:
        favorite[0].delete()
    print(next)
    return redirect('product', product_id)

def addToCart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        product = Product.objects.get(id=product_id)
    except:
        raise Http404
    
    if request.user == product.seller.user or product.stock == 0:
        raise Http404
    
    productInCart = list(ProductInCart.objects.filter(product=product, user=request.user))
    if len(productInCart):
        raise Http404
    
    newProductInCart = ProductInCart(user=request.user, product=product, count=1, date=datetime.datetime.now())
    newProductInCart.save()

    path = getUrl(int(request.GET.get('page')), request.GET.get('inStock'), request.GET.get('withDiscount'), request.GET.get('withRating'))
    if request.GET.get('pathName'):
        if request.GET.get('sortKey'):
            if request.GET.get('id'):
                return redirect(reverse(request.GET.get('pathName'), args=[int(request.GET.get('id')), int(request.GET.get('sortKey'))]) + path)
            else:
                return redirect(reverse(request.GET.get('pathName'), args=[int(request.GET.get('sortKey'))]) + path)
        
    return redirect('product', product_id)

def plusProductInCart(request, product_id):
    if not request.user.is_authenticated:
        raise Http404
    try:
        product = Product.objects.get(id=product_id)
        productInCart = ProductInCart.objects.get(user=request.user, product=product)
    except:
        raise Http404
    
    if product.seller.user == request.user:
        raise Http404

    productInCart.count += 1
    if productInCart.count < 1:
        productInCart.delete()
    else:
        productInCart.save()

    path = getUrl(int(request.GET.get('page')), request.GET.get('inStock'), request.GET.get('withDiscount'), request.GET.get('withRating'))
    if request.GET.get('pathName'):
        if request.GET.get('sortKey'):
            if request.GET.get('id'):
                return redirect(reverse(request.GET.get('pathName'), args=[int(request.GET.get('id')), int(request.GET.get('sortKey'))]) + path)
            else:
                return redirect(reverse(request.GET.get('pathName'), args=[int(request.GET.get('sortKey'))]) + path)
            
    return redirect('product', product_id)

def minusProductInCart(request, product_id):
    if not request.user.is_authenticated:
        raise Http404
    try:
        product = Product.objects.get(id=product_id)
        productInCart = ProductInCart.objects.get(user=request.user, product=product)
    except:
        raise Http404
    
    if product.seller.user == request.user:
        raise Http404

    productInCart.count -= 1
    if productInCart.count < 1:
        productInCart.delete()
    else:
        productInCart.save()
    
    path = getUrl(int(request.GET.get('page')), request.GET.get('inStock'), request.GET.get('withDiscount'), request.GET.get('withRating'))
    if request.GET.get('pathName'):
        if request.GET.get('sortKey'):
            if request.GET.get('id'):
                return redirect(reverse(request.GET.get('pathName'), args=[int(request.GET.get('id')), int(request.GET.get('sortKey'))]) + path)
            else:
                return redirect(reverse(request.GET.get('pathName'), args=[int(request.GET.get('sortKey'))]) + path)
            
    return redirect('product', product_id)    