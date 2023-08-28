from django.shortcuts import render

from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import redirect
from django.urls.base import reverse_lazy, reverse
from django.views.generic import *
from django.http import Http404

from django.core.paginator import Paginator
from django.core.mail import EmailMessage

from django.conf import settings

from .models import *
from .utils import *
from main.utils import *

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
    
    productInCart = list(ProductInCart.objects.filter(product=product, user=request.user, is_active=True))
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
        productInCart = ProductInCart.objects.get(user=request.user, product=product, is_active=True)
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
        productInCart = ProductInCart.objects.get(user=request.user, product=product, is_active=True)
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
        productInCart = ProductInCart.objects.get(user=request.user, product=product, is_active=True)
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
    
    productsInCart = list(ProductInCart.objects.filter(user=request.user, is_active=True))
    productsInCart.sort(key=lambda x: x.date, reverse=True)

    totalPrice = sum(x.product.getPriceWithDiscount() * x.count for x in productsInCart)

    title = 'Корзина'

    context={
        'title': title,
        'products': productsInCart,
        'totalPrice':totalPrice,
    }

    return render(request, "buyers/cartList.html", context=context)

def makeOrder(request):
    if not request.user.is_authenticated:
         raise Http404
    
    productInCart = list(ProductInCart.objects.filter(user=request.user, is_active=True))
    if len(productInCart) == 0:
        raise Http404
    totalPrice = 0
    for p in productInCart:
        if p.count <= p.product.stock:
            totalPrice += p.count * p.product.getPriceWithDiscount()
        else:
            p.count = p.product.stock
            if p.product.stock == 0:
                p.delete()
                continue
            p.save()
            totalPrice += p.count * p.product.getPriceWithDiscount()
        p.product.stock -= p.count
        p.product.save()
        p.is_active = False
        p.save()
    address = request.GET.get('address')
    newOrder = Order(date=datetime.datetime.now(), user=request.user, total_price=totalPrice)
    newOrder.save()
    email = EmailMessage(f'Заказ №{newOrder.id}',
                         f'Адрес: {address}. Сумма: {totalPrice} ₽.\n2023 © Tech-Katalog',
                         settings.DEFAULT_FROM_EMAIL,
                         to=[request.user.email])
    email.send()
    return redirect('cart')

def forgotLoginPage(request):

    context={
        'title': 'Восстановить логин ',
        'text': 'Если Вы были зарегистрированы на сайте, то на Вашу почту придет письмо с логином',
        'formAction': 'forgotLogin',
        'placeholder': 'Ваша почта',
        'inputName': 'email',
    }

    return render(request, "main/forgot.html", context=context)

def forgotLogin(request):
    email = request.GET.get('email')
    user = list(User.objects.filter(email=email))
    if len(user) == 0:
        return redirect('login')
    text = ''
    if len(user) > 1:
        for i in range(len(user)):
            text += user[i].username
            if i != len(user) - 1:
                text += ', '
    else:
        text += user[0].username

    if len(user) == 1:
        email = EmailMessage(f'Восстановление логина',
                         f'Найден логин: {text}.\n2023 © Tech-Katalog',
                         settings.DEFAULT_FROM_EMAIL,
                         to=[email])
    else:
        email = EmailMessage(f'Восстановление логина',
                            f'Найдены логины: {text}.\n2023 © Tech-Katalog',
                            settings.DEFAULT_FROM_EMAIL,
                            to=[email])
    email.send()
    return redirect('login')