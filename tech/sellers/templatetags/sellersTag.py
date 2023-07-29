from django import template

from ..models import *

register = template.Library()

@register.simple_tag
def checkIsSeller(user):
    seller = list(Seller.objects.filter(user=user))
    if len(seller):
        return True
    return False