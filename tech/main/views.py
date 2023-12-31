from django.shortcuts import render

from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import redirect
from django.urls.base import reverse_lazy, reverse
from django.views.generic import *
from django.http import Http404, HttpResponseRedirect
from django.db.models import Q

from .forms import *
from .models import *
from .utils import *

from sellers.models import *

import datetime

from django.core.paginator import Paginator

class Index(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        
        context = super().get_context_data(**kwargs)
        categories = list(Category.objects.all())
        
        context["categories"] = categories
        return context
    
def categoryProductList(request, category_id, sort_key):
    try:
        category = Category.objects.get(id=category_id)
    except:
        raise Http404
    products = list(Product.objects.filter(category=category))
    
    sortedProducts = productSort(products, sort_key, inStock=request.GET.get('inStock'),
                                 withDiscount=request.GET.get('withDiscount'), withRating=request.GET.get('withRating'))
    
    paginator = Paginator(sortedProducts, 1)

    page_number = request.GET.get("page")
    page_objects = paginator.get_page(page_number)
    
    title = category.plural_name

    context={
        'title': title,
        'page_objects':page_objects,
        'id': category_id,
        'sortKey': sort_key,
        'pathName': request.resolver_match.url_name,
    }
    return render(request, "main/productListWithId.html", context=context)

def allProductsList(request, sort_key):
    products = list(Product.objects.all())
    
    sortedProducts = productSort(products, sort_key, inStock=request.GET.get('inStock'),
                                 withDiscount=request.GET.get('withDiscount'), withRating=request.GET.get('withRating'))

    paginator = Paginator(sortedProducts, 2)

    page_number = request.GET.get("page")
    page_objects = paginator.get_page(page_number)
    
    title = 'Все товары'

    context={
        'title': title,
        'page_objects':page_objects,
        'sortKey': sort_key,
        'pathName': request.resolver_match.url_name
    }
    return render(request, "main/productList.html", context=context)

def search(request):
    if not request.GET.get('search'):
        return redirect('all', 1)
    return redirect(reverse('search', args=[1]) + f'?search={request.GET.get("search")}')

def searchPage(request, sort_key):
    products = list(Product.objects.all())

    if not request.GET.get('search'):
        return redirect('all', 1)

    selectedProducts = []
    searchText = request.GET.get('search')
    searchWords = searchText.split()

    for p in products:
        for w in searchWords:
            if w.lower() in p.name.lower() or p.name.lower() in w.lower():
                selectedProducts.append(p)
                break

    sortedProducts = productSort(selectedProducts, sort_key, inStock=request.GET.get('inStock'),
                                 withDiscount=request.GET.get('withDiscount'), withRating=request.GET.get('withRating'))

    paginator = Paginator(sortedProducts, 2)

    page_number = request.GET.get("page")
    page_objects = paginator.get_page(page_number)
    
    title = f'Поиск: \"{searchText}\"'

    context={
        'title': title,
        'page_objects':page_objects,
        'sortKey': sort_key,
        'pathName': request.resolver_match.url_name,
        'searchText': searchText,
    }
    return render(request, "main/productList.html", context=context)

def productPage(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except:
        raise Http404
    images = list(ProductImage.objects.filter(product=product))
    seller = Seller.objects.get(id=product.seller.id)
    try:
        discount = Discount.objects.get(product=product)
    except:
        discount = False
    try:
        productRating = ProductRating.objects.get(user=request.user, product=product)
    except:
        productRating = False
    allReviews = list(ProductRating.objects.filter(product=product))
    reviewsCount = len(allReviews)
    avgRating = product.getAvgProductRating()
    if request.user.is_authenticated:
        revs = list(ProductRating.objects.filter(product=product).exclude(user=request.user))
    else:
        revs = list(ProductRating.objects.filter(product=product))
    revs.sort(key=lambda x: x.date, reverse=True)
    reviewsWithoutUser = []
    for r in revs:
        if r.text or r.plus or r.minus:
            reviewsWithoutUser.append(r)
    reviewsWithTextCount = len(reviewsWithoutUser)
    reviewsWithTextWithoutUser = reviewsWithTextCount
    if productRating:
        if productRating.text or productRating.plus or productRating.minus:
            reviewsWithTextCount += 1
    if len(reviewsWithoutUser) > 3:
        reviewsWithoutUser = reviewsWithoutUser[:3]
    context={
        'product': product,
        'images': images,
        'seller': seller,
        'discount': discount,
        'path': request.path.replace('/', '-'),
        'productRating': productRating,
        'reviews': allReviews,
        'reviewsCount': reviewsCount,
        'avgRating': avgRating,
        'reviewsWithoutUser': reviewsWithoutUser,
        'moreThen3Reviews': reviewsWithTextWithoutUser > 3,
        'reviewsWithTextCount': reviewsWithTextCount,
    }

    return render(request, 'main/productPage.html', context=context)

def deleteImage(request, product_id, image_id):
    try:
        product = Product.objects.get(id=product_id)
        image = ProductImage.objects.get(id=image_id)
        seller = Seller.objects.get(user=request.user)
    except:
        raise Http404
    image.delete()
    return redirect('product', product_id)

def makeProductReview(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except:
        raise Http404
    if (not request.user.is_authenticated) or request.user == product.seller.user :
        raise Http404
    if len(ProductRating.objects.filter(product=product, user=request.user)):
        productRatingExist = True
    else:
        productRatingExist = False
    if productRatingExist:
        productRating = ProductRating.objects.get(user=request.user, product=product)
        if request.GET.get('rating'):
            productRating.value = int(request.GET.get('rating'))
            productRating.date = datetime.datetime.now()
        productRating.text = request.GET.get('reviewText')
        productRating.plus = request.GET.get('plusText')
        productRating.minus = request.GET.get('minusText')
        productRating.date = datetime.datetime.now()
        productRating.save()
    else:
        if request.GET.get('rating'):
            productRating = ProductRating(value=int(request.GET.get('rating')), date=datetime.datetime.now(), user=request.user, product=product)
            if request.GET.get('reviewText'):
                productRating.text = request.GET.get('reviewText')
            if request.GET.get('plusText'):
                productRating.plus = request.GET.get('plusText')
            if request.GET.get('minusText'):
                productRating.minus = request.GET.get('minusText')
            productRating.save()
    return redirect('product', product_id)

def productReviewsPage(request, product_id, sort_key):
    try:
        product = Product.objects.get(id=product_id)
    except:
        raise Http404
    try:
        productRating = ProductRating.objects.get(user=request.user, product=product)
    except:
        productRating = False
    avgRating = product.getAvgProductRating()
    reviewsCount = product.getProductRatingCount()
    
    allReviews = list(ProductRating.objects.filter(product=product))
    if request.user.is_authenticated:
        revs = list(ProductRating.objects.filter(product=product).exclude(user=request.user))
    else:
        revs = list(ProductRating.objects.filter(product=product))
    if len(revs) < 3:
        raise Http404
    if sort_key == 1: 
        revs.sort(key=lambda x: x.date, reverse=True)
    elif sort_key == 2:
        revs.sort(key=lambda x: x.date, reverse=False)
    elif sort_key == 3:
        revs.sort(key=lambda x: x.value, reverse=False)
    elif sort_key == 4:
        revs.sort(key=lambda x: x.value, reverse=True)
    reviewsWithoutUser = []
    for r in revs:
        if r.text or r.plus or r.minus:
            reviewsWithoutUser.append(r)
    reviewsWithTextCount = len(reviewsWithoutUser)
    if productRating:
        if productRating.text or productRating.plus or productRating.minus:
            reviewsWithTextCount += 1

    paginator = Paginator(reviewsWithoutUser, 3)

    page_number = request.GET.get("page")
    page_objects = paginator.get_page(page_number)

    title = product.name
    id = product.id

    context={
        'productRating': productRating,
        'page_objects': page_objects,
        'reviewsCount': reviewsCount,
        'avgRating': avgRating,
        'reviewsWithoutUser': reviewsWithoutUser,
        'reviewsWithTextCount': reviewsWithTextCount,
        'sortKey': sort_key,
        'title': title,
        'id': id,
        'pathName': request.resolver_match.url_name,
        'name': 'product',
    }

    return render(request, 'main/reviewsPage.html', context=context)



def sellerPage(request, seller_id):
    try:
        seller = Seller.objects.get(id=seller_id)
    except:
        raise Http404
    
    if request.user.is_authenticated:
        if seller.user.id == request.user.id:
            return redirect('sellerArea')

    if request.user.is_authenticated:
        try:
            sellerRating = SellerRating.objects.get(user=request.user, seller=seller)
        except:
            sellerRating = False
    else:
        sellerRating = False
    avgRating = seller.getAvgSellerRating()
    ratingCount = seller.getSellerRatingCount()
    
    allReviews = list(SellerRating.objects.filter(seller=seller))

    if request.user.is_authenticated:
        revs = list(SellerRating.objects.filter(seller=seller).exclude(user=request.user))
    else:
        revs = list(SellerRating.objects.filter(seller=seller))
    revs.sort(key=lambda x: x.date, reverse=True)
    reviewsWithoutUser = []
    for r in revs:
        if r.text:
            reviewsWithoutUser.append(r)

    reviewsWithTextCount = len(reviewsWithoutUser)

    if len(reviewsWithoutUser) > 3:
        moreThen3 = True
        reviewsWithoutUser = reviewsWithoutUser[:3]
    else:
        moreThen3 = False
    
    if sellerRating:
        if sellerRating.text:
            reviewsWithTextCount += 1
    context={
        'seller':seller,
        'sellerRating': sellerRating,
        'avgRating': avgRating,
        'reviewsCount': ratingCount,
        'reviews': allReviews,
        'reviewsWithoutUser': reviewsWithoutUser,
        'moreThen3Reviews': moreThen3,
        'reviewsWithTextCount': reviewsWithTextCount,
    }

    return render(request, 'sellers/sellerPage.html', context=context)

def makeSellerReview(request, seller_id):
    try:
        seller = Seller.objects.get(id=seller_id)
    except:
        raise Http404
    if (not request.user.is_authenticated) or request.user == seller.user:
        raise Http404
    sellerRating = list(SellerRating.objects.filter(user=request.user, seller=seller))

    if len(sellerRating) == 0:
        sellerRatingExist = False
    else:
        sellerRatingExist = True
    
    if sellerRatingExist:
        if request.GET.get('rating'):
            sellerRating[0].value = int(request.GET.get('rating'))
        sellerRating[0].text = request.GET.get('reviewText')
        sellerRating[0].date = datetime.datetime.now()
        sellerRating[0].save()
    else:
        if request.GET.get('rating'):
            newSellerRating = SellerRating(value=int(request.GET.get('rating')), date=datetime.datetime.now(), user=request.user, seller=seller)
            if request.GET.get('reviewText'):
                newSellerRating.text = request.GET.get('reviewText')
            newSellerRating.save()
    return redirect('seller', seller_id)

def sellerReviewsPage(request, seller_id, sort_key):
    try:
        seller = Seller.objects.get(id=seller_id)
    except:
        raise Http404
    try:
        sellerRating = SellerRating.objects.get(user=request.user, seller=seller)
    except:
        sellerRating = False
    allReviews = list(SellerRating.objects.filter(seller=seller))
    reviewsCount = len(allReviews)
    try:
        avgRating = round(sum(r.value for r in allReviews) / len(allReviews), 2)
    except:
        avgRating = 0
    if avgRating % 1 == 0:
        avgRating = int(avgRating)
    if request.user.is_authenticated:
        revs = list(SellerRating.objects.filter(seller=seller).exclude(user=request.user))
    else:
        revs = list(SellerRating.objects.filter(seller=seller))
    if sort_key == 1: 
        revs.sort(key=lambda x: x.date, reverse=True)
    elif sort_key == 2:
        revs.sort(key=lambda x: x.date, reverse=False)
    elif sort_key == 3:
        revs.sort(key=lambda x: x.value, reverse=False)
    elif sort_key == 4:
        revs.sort(key=lambda x: x.value, reverse=True)
    reviewsWithoutUser = []
    for r in revs:
        if r.text or r.plus or r.minus:
            reviewsWithoutUser.append(r)
    reviewsWithTextCount = len(reviewsWithoutUser)
    if reviewsWithTextCount <= 3:
        raise Http404
    if sellerRating:
        if sellerRating.text:
            reviewsWithTextCount += 1
    
    paginator = Paginator(reviewsWithoutUser, 3)

    page_number = request.GET.get("page")
    page_objects = paginator.get_page(page_number)

    title = seller.name
    id = seller.id


    context={
        'sellerRating': sellerRating,
        'reviews': allReviews,
        'reviewsCount': reviewsCount,
        'avgRating': avgRating,
        'page_objects':page_objects,
        'reviewsWithTextCount': reviewsWithTextCount,
        'sortKey': sort_key,
        'title': title,
        'id': id,
        'pathName': request.resolver_match.url_name,
        'name': 'seller',
    }

    return render(request, 'main/reviewsPage.html', context=context)

class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'main/form.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Регистрация'
        context["button_text"] = "Зарегистрироваться"
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

class Login(LoginView):
    form_class = LoginForm
    template_name = 'main/form.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Вход"
        context["button_text"] = "Войти"
        context['noaccount_text'] = 'Нет аккаунта? '
        context['signupurl'] = 'Создайте!'
        return context

    def get_success_url(self):
        return reverse_lazy('index')

class ChangeUserData(LoginRequiredMixin, UpdateView):
    form_class = ChangeUserDataForm
    template_name = 'main/form.html'
    success_url = reverse_lazy('index')
    login_url = reverse_lazy('login')

    def get_object(self):
        return self.request.user

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактировать данные"
        context["button_text"] = "Сохранить"
        return context

class ChangePass(LoginRequiredMixin, PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'main/form.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Изменить пароль"
        context["button_text"] = "Изменить"
        return context

    def form_valid(self, form):
        return super().form_valid(form)
    
def logout_user(request):
    logout(request)
    return redirect('login')