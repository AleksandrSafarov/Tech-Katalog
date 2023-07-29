from django.shortcuts import render, redirect
from django.views.generic import *

from .models import *
from .forms import *
from .utils import *

def sellerPage(request, seller_id):
    seller = Seller.objects.get(id=seller_id)
    if request.user.is_authenticated:
        if seller.user.id == request.user.id:
            return redirect('sellerArea')

    context={
        'seller':seller,
    }

    return render(request, 'sellers/sellerPage.html', context=context)

class SellerArea(IsSellerMixin, TemplateView):
    template_name = 'sellers/sellerArea.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        
        context = super().get_context_data(**kwargs)
        seller = Seller.objects.get(user=self.request.user)
        
        context["seller"] = seller
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