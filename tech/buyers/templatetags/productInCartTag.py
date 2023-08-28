from django import template
from django.contrib.auth.models import User

from main.models import Product
from ..models import ProductInCart

register = template.Library()

@register.simple_tag
def isProductInCart(product_id, user_id=0):
    if not user_id:
        return False
    try:
        product = Product.objects.get(id=product_id)
        user = User.objects.get(id=user_id)
    except:
        return False
    productInCart = list(ProductInCart.objects.filter(product=product, user=user, is_active=True))
    if len(productInCart):
        return True
    return False

@register.simple_tag
def getProductInCartCount(product_id, user_id=0):
    if not user_id:
        return 0
    try:
        product = Product.objects.get(id=product_id)
        user = User.objects.get(id=user_id)
    except:
        return 0
    productInCart = list(ProductInCart.objects.filter(product=product, user=user, is_active=True))
    if len(productInCart):
        return productInCart[0].count
    return 0
    