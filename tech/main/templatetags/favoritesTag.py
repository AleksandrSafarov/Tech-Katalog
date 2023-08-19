from django import template
from django.contrib.auth.models import User

from ..models import *
from buyers.models import Favorites

register = template.Library()

@register.simple_tag
def isFavorite(product_id, user_id=0):
    if user_id == 0:
        return False
    try:
        product = Product.objects.get(id=product_id)
        user = User.objects.get(id=user_id)
    except:
        return False
    try:
        favorite = Favorites.objects.get(product=product, user=user)
    except:
        return False
    return True