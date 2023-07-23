from tech.celery import app
import time
from .models import *


@app.task #регистриуем таску
def repeat_order_make():
    print('adsdasd')
    #obj = Category.objects.get_or_create(name=f'{time.time()}11111111111111111', plural_name='1111')
    return "необязательная заглушка"