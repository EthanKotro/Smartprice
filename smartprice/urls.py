from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("pricefinder.urls")),
    path('admin/', admin.site.urls),
    path('pricefinder/', include('pricefinder.urls')), 
]