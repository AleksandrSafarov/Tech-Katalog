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