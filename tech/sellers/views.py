from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import *

from .models import *
from .forms import *
from .utils import *
from main.models import *

from main.models import *
from main.utils import *

import datetime


def changeDataPage(request, product_id, previous_url):
    try:
        product = Product.objects.get(id=product_id)
        seller = Seller.objects.get(user=request.user)
    except:
        raise Http404
    context={
        'product':product,
        'previous_url': previous_url.replace('-', '/')
    }
    
    return render(request, 'sellers/changeDataPage.html', context=context)

def changeDataPageWithoutPrevious(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        seller = Seller.objects.get(user=request.user)
    except:
        raise Http404
    
    return redirect('newData', product_id, '-management-')

def changeData(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        seller = Seller.objects.get(user=request.user)
    except:
        raise Http404
    if request.GET.get('newPrice'):
        newPrice = int(request.GET.get('newPrice'))
        product.price = newPrice
        product.save()
    if request.GET.get('newStock') or request.GET.get('newStock') == 0:
        newStock = int(request.GET.get('newStock'))
        product.stock = newStock
        product.save()
        changeStock(product)
    if request.GET.get('newDescription'):
        newDescription = request.GET.get('newDescription')
        product.description = newDescription
        product.save()
    next = request.GET.get('next', '/')
    return HttpResponseRedirect(next)

def addProductImage(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        seller = Seller.objects.get(user=request.user)
    except:
        raise Http404
    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.product = product
            form.save()
            return redirect('product', product_id)
    else:
        form = ProductImageForm
    context={
        'title': 'Добавить изображение',
        'button_text': 'Добавить',
        'form': form
    }
    return render(request, 'main/form.html', context=context)

def makeDiscountPage(request, product_id, previous_url):
    try:
        product = Product.objects.get(id=product_id)
        seller = Seller.objects.get(user=request.user)
    except:
        raise Http404
    try:
        discount = Discount.objects.get(product=product)
    except:
        discount = False
    context={
        'product': product,
        'discount': discount,
        'previous_url': previous_url.replace('-', '/')
    }
    
    return render(request, 'sellers/makeDiscountPage.html', context=context)

def makeDiscountPageWithoutPrevious(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        seller = Seller.objects.get(user=request.user)
    except:
        raise Http404
    
    return redirect('makeDiscountPage', product_id, '-management-')

def makeDiscount(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        seller = Seller.objects.get(user=request.user)
    except:
        raise Http404
    discount = list(Discount.objects.filter(product=product))
    print(len(discount))
    if len(discount):
        if request.GET.get('newDiscountValue'):
            newDiscountValue = int(request.GET.get('newDiscountValue'))
            discount[0].value = newDiscountValue
            discount[0].save()
        if request.GET.get('addDays'):
            addDays = int(request.GET.get('addDays'))
            newFinishDate = datetime.datetime.now() + datetime.timedelta(days=addDays)
            newFinishDate = newFinishDate.replace(hour=23, minute=59, second=59)
            discount[0].finish_date = newFinishDate
            discount[0].save()
    else:
        if request.GET.get('newDiscountValue') and request.GET.get('addDays'):
            newDiscountValue = int(request.GET.get('newDiscountValue'))
            addDays = int(request.GET.get('addDays'))
            newFinishDate = datetime.datetime.now() + datetime.timedelta(days=addDays)
            newFinishDate = newFinishDate.replace(hour=23, minute=59, second=59)
            newDiscount = Discount(value=newDiscountValue, product=product, finish_date=newFinishDate)
            newDiscount.save()
        else:
            return redirect('makeDiscountPage')
    
    next = request.GET.get('next', '/')
    return HttpResponseRedirect(next)


class SellerArea(IsSellerMixin, TemplateView):
    template_name = 'sellers/sellerArea.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        seller = Seller.objects.get(user=self.request.user)
        
        context["seller"] = seller
        return context

class ProductManagement(IsSellerMixin, TemplateView):
    template_name = 'sellers/productManagement.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        seller = Seller.objects.get(user=self.request.user)
        products = list(Product.objects.filter(seller=seller))

        context['products'] = products
        context['total_obj'] = len(products)
        context['path'] = self.request.path.replace('/', '-')
        return context


class CreateSeller(IsNotSellerMixin, CreateView):
    form_class = CreateSellerForm
    template_name = 'main/form.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Регистрация продавца'
        context["button_text"] = "Зарегистрироваться"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect('sellerArea')

class CreateProduct(IsSellerMixin, CreateView):
    form_class = CreateProductForm
    template_name = 'main/form.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Добавить товар'
        context["button_text"] = "Добавить"
        return context

    def form_valid(self, form):
        seller = Seller.objects.get(user=self.request.user)
        form.instance.seller = seller
        form.save()
        return redirect('productManagement')