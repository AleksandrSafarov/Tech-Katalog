def getUrl(page, inStock=False, withDiscount=False, withRating=False):
    res = f'?page={page}&'
    if inStock == 'on':
        res += f'inStock={inStock}&'
    if withDiscount == 'on':
        res += f'withDiscount={withDiscount}&'
    if withRating == 'on':
        res += f'withRating={withRating}'
    return res