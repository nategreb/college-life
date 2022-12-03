from django.contrib import admin
from django.urls import path, include
import allauth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]
