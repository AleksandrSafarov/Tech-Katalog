from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from tech import settings

urlpatterns = [
    path('', include('main.urls')),
    path('', include('sellers.urls')),
    path('admin/', admin.site.urls, name='admin'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)