from django import forms
from django.contrib.auth.forms import *

from .models import *
from main.models import Product, Category

class CreateSellerForm(forms.ModelForm):
    name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': "Короткое название (Пример: \"CompanyName\")"})
        )
    full_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': "Полное название (Пример: ООО \"CompanyName\")"})
    )
    address = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': "Адрес"})
    )
    description = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'placeholder': "Описание (необязательно)"})
    )
    image = forms.ImageField(
        label="Логотип",
                             )
    class Meta:
        model = Seller
        fields = ('name', 'full_name', 'address', 'description', 'image')

class CreateProductForm(forms.ModelForm):
    name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': "Название"})
        )
    category = forms.ModelChoiceField(
        label="Категория товара",
        queryset=Category.objects.all()
    )
    price = forms.IntegerField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': "Цена (₽)", 
                                      'min':'1', 
                                      'max':'100000000000'})
    )
    stock = forms.IntegerField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': "Количество",
                                      'min':'1'})
    )
    description = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'placeholder': "Описание товара"})
    )
    main_image = forms.ImageField(
        label="Главное изображение товара"
        )
    class Meta:
        model = Product
        fields = ('name', 'category', 'price', 'stock', 'description', 'main_image')