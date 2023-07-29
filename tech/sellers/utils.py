from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.core.exceptions import PermissionDenied

from .models import *

class IsSellerMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        seller = list(Seller.objects.filter(user=self.request.user))
        if len(seller):
            return True
        raise PermissionDenied
    
class IsNotSellerMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        seller = list(Seller.objects.filter(user=self.request.user))
        if not len(seller):
            return True
        raise PermissionDenied