from buyers.models import *

def productSort(products, sort_key, inStock=False, withDiscount=False, withRating=False):
    if sort_key == 1:
        products.sort(key=lambda x: x.id, reverse=True)
    elif sort_key == 2:
        products.sort(key=lambda x: x.getAvgProductRating(), reverse=False)
    elif sort_key == 3:
        products.sort(key=lambda x: x.getAvgProductRating(), reverse=True)
    elif sort_key == 4:
        products.sort(key=lambda x: x.getProductRatingCount(), reverse=False)
    elif sort_key == 5:
        products.sort(key=lambda x: x.getProductRatingCount(), reverse=True)
    elif sort_key == 6:
        products.sort(key=lambda x: x.getPriceWithDiscount(), reverse=False)
    elif sort_key == 7:
        products.sort(key=lambda x: x.getPriceWithDiscount(), reverse=True)

    if inStock == 'on':
        products1 = []
        for p in products:
            if p.stock != 0:
                products1.append(p)
    else:
        products1 = products
    
    if withDiscount == 'on':
        products2 = []
        for p in products1:
            if p.hasDiscount():
                products2.append(p)
    else:
        products2 = products1
    
    if withRating == 'on':
        products3 = []
        for p in products2:
            if p.getProductRatingCount():
                products3.append(p)
    else:
        products3 = products2
    
    return products3

def changeStock(product):
    productInCart = list(ProductInCart.objects.filter(product=product))
    for p in productInCart:
        print(p.count)
        print(product.stock)
        if p.count > product.stock:
            print('*')
            p.count = product.stock
            p.save()
        if product.stock == 0:
            p.delete()