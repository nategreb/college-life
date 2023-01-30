from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),

    # third party
    path('accounts/', include('allauth.urls')),
    path('reviews/', include('reviews.urls')),

    # apps
    path('', home, name='home'),
    path('colleges/', include('colleges.urls'), name='colleges'),

    # debugging
    path('__debug__/', include('debug_toolbar.urls')),
]
