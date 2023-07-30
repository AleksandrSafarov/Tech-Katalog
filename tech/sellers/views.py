from django.shortcuts import render, redirect
from django.views.generic import *

from .models import *
from .forms import *
from .utils import *

from main.models import *

def sellerPage(request, seller_id):
    seller = Seller.objects.get(id=seller_id)
    if request.user.is_authenticated:
        if seller.user.id == request.user.id:
            return redirect('sellerArea')

    context={
        'seller':seller,
    }

    return render(request, 'sellers/sellerPage.html', context=context)

def changeStockPage(request, product_id):
    product = Product.objects.get(id=product_id)
    seller = Seller.objects.get(user=request.user)
    if not seller:
        raise Http404
    if not product:
        raise Http404
    context={
        'product':product,
    }
    
    return render(request, 'sellers/changeStockPage.html', context=context)

def changeStock(request, product_id):
    product = Product.objects.get(id=product_id)
    seller = Seller.objects.get(user=request.user)
    if not seller:
        raise Http404
    if not product:
        raise Http404
    if request.GET.get('newStock'):
        newStock = int(request.GET.get('newStock'))
        product.stock = newStock
        product.save()
    return redirect('productManagement')

def changePricePage(request, product_id):
    product = Product.objects.get(id=product_id)
    seller = Seller.objects.get(user=request.user)
    if not seller:
        raise Http404
    if not product:
        raise Http404
    context={
        'product':product,
    }
    
    return render(request, 'sellers/changePricePage.html', context=context)

def changePrice(request, product_id):
    product = Product.objects.get(id=product_id)
    seller = Seller.objects.get(user=request.user)
    if not seller:
        raise Http404
    if not product:
        raise Http404
    if request.GET.get('newPrice'):
        newPrice = int(request.GET.get('newPrice'))
        product.price = newPrice
        product.save()
    return redirect('productManagement')


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
        return redirect('index')