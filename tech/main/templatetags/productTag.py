from django import template

register = template.Library()

@register.simple_tag
def getPriceWithDiscount(price, discountValue):
    discount = 1 - (discountValue / 100)
    priceWithDiscount = int(price * discount)
    if priceWithDiscount == 0:
        priceWithDiscount = 1
    return priceWithDiscount