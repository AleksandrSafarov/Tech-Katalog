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
from main.utils import *

from django.core.paginator import Paginator

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

    try:
        path = getUrl(int(request.GET.get('page')), request.GET.get('inStock'), request.GET.get('withDiscount'), request.GET.get('withRating'))
    except:
        path = ''
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
    
    try:
        path = getUrl(int(request.GET.get('page')), request.GET.get('inStock'), request.GET.get('withDiscount'), request.GET.get('withRating'))
    except:
        path = ''

    if request.GET.get('pathName') == 'cart':
        return redirect('cart')

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
        
    try:
        path = getUrl(int(request.GET.get('page')), request.GET.get('inStock'), request.GET.get('withDiscount'), request.GET.get('withRating'))
    except:
        path = ''
        
    if request.GET.get('pathName') == 'cart':
        return redirect('cart')
    
    if request.GET.get('pathName'):
        if request.GET.get('sortKey'):
            if request.GET.get('id'):
                return redirect(reverse(request.GET.get('pathName'), args=[int(request.GET.get('id')), int(request.GET.get('sortKey'))]) + path)
            else:
                return redirect(reverse(request.GET.get('pathName'), args=[int(request.GET.get('sortKey'))]) + path)
            
    return redirect('product', product_id)

def deleteProductInCart(request, product_id):
    if not request.user.is_authenticated:
        redirect('login')
    print('*')
    try:
        product = Product.objects.get(id=product_id)
        productInCart = ProductInCart.objects.get(user=request.user, product=product)
    except:
        raise Http404
    
    
    productInCart.delete()
        
    try:
        path = getUrl(int(request.GET.get('page')), request.GET.get('inStock'), request.GET.get('withDiscount'), request.GET.get('withRating'))
    except:
        path = ''
        
    if request.GET.get('pathName') == 'cart':
        return redirect('cart')

    if request.GET.get('pathName'):
        if request.GET.get('sortKey'):
            if request.GET.get('id'):
                return redirect(reverse(request.GET.get('pathName'), args=[int(request.GET.get('id')), int(request.GET.get('sortKey'))]) + path)
            else:
                return redirect(reverse(request.GET.get('pathName'), args=[int(request.GET.get('sortKey'))]) + path)
            
    return redirect('product', product_id)

def favoritePage(request, sort_key):
    if not request.user.is_authenticated:
        redirect('login')

    favoriteProducts = list(Favorites.objects.filter(user=request.user))
    products = []
    for f in favoriteProducts:
        products.append(f.product)
    sortedProducts = productSort(products, sort_key, inStock=request.GET.get('inStock'),
                                 withDiscount=request.GET.get('withDiscount'), withRating=request.GET.get('withRating'))
    
    paginator = Paginator(sortedProducts, 2)

    page_number = request.GET.get("page")
    page_objects = paginator.get_page(page_number)
    title = 'Избранное'

    context={
        'title': title,
        'page_objects':page_objects,
        'sortKey': sort_key,
        'pathName': request.resolver_match.url_name
    }
    return render(request, "main/productList.html", context=context)

def cartPage(request):
    if not request.user.is_authenticated:
        redirect('login')
    
    productsInCart = list(ProductInCart.objects.filter(user=request.user))
    productsInCart.sort(key=lambda x: x.date, reverse=True)

    totalPrice = sum(x.product.getPriceWithDiscount() * x.count for x in productsInCart)

    title = 'Корзина'

    context={
        'title': title,
        'products': productsInCart,
        'totalPrice':totalPrice,
    }

    return render(request, "buyers/cartList.html", context=context)