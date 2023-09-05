from main.models import Popularity
import datetime

def getUrl(page=0, inStock=False, withDiscount=False, withRating=False):
    res = ''
    if page:
        res = f'?page={page}&'
        if inStock == 'on':
            res += f'inStock={inStock}&'
        if withDiscount == 'on':
            res += f'withDiscount={withDiscount}&'
        if withRating == 'on':
            res += f'withRating={withRating}'
    return res

def makePopularity(productsInCart):
    for p in productsInCart:
        for i in range(p.count):
            newPopularity = Popularity(product=p.product, finish_date=datetime.datetime.now() + datetime.timedelta(days=30))
            newPopularity.save()