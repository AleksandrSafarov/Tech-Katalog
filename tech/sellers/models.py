from django.db import models
from django.contrib.auth.models import User


class Seller(models.Model):
    name = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=150)
    description = models.TextField(null=True)
    is_sertificated = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/sellers/')

    def __str__(self):
        return self.name
    
    def getAvgSellerRating(self):
        reviews = list(SellerRating.objects.filter(seller=self))
        if len(reviews) == 0:
            return 0
        avgRating = round(sum(r.value for r in reviews) / len(reviews), 2)
        if avgRating % 1 == 0:
            return int(avgRating)
        return avgRating
    
    def getSellerRatingCount(self):
        return len(list(SellerRating.objects.filter(seller=self)))


class SellerRating(models.Model):
    value = models.IntegerField(default=1)
    text = models.TextField(null=True)
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

    def __str__(self):
        return self.seller.name + ': ' + self.user.username
    
    def getdate(self):
        return str(self.date.day).zfill(2)+'.'+str(self.date.month).zfill(2)+'.'+str(self.date.year)