from django import forms
from django.contrib.auth.forms import *

from .models import *

class CreateSellerForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Короткое название (Пример: \"CompanyName\")"})
        )
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Полное название (Пример: ООО \"CompanyName\")"})
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Адрес"})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': "Описание (необязательно)"})
    )
    image = forms.ImageField(
        )
    class Meta:
        model = Seller
        fields = ('name', 'full_name', 'address', 'description', 'image')

class ChangeStockForm(forms.Form):
    newStock = forms.IntegerField()