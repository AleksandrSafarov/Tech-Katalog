from tech.celery import app
import time
from .models import *
import datetime
import pytz

@app.task #регистриуем таску
def checkFinishDate():
    discounts = Discount.objects.all()
    utc = pytz.UTC
    currentDateTime = datetime.datetime.now().replace(tzinfo=utc)
    for d in discounts:
        if d.finish_date.replace(tzinfo=utc) < currentDateTime:
            d.delete()
    popularity = list(Popularity.objects.all())
    for p in popularity:
        if p.finish_date.replace(tzinfo=utc) < currentDateTime:
            p.delete()
    return "задача выполнена"