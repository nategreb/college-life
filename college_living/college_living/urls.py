from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),

    # third party
    path('accounts/', include('allauth.urls')),

    # apps
    path('', home, name='home'),
    path('colleges/', include('colleges.urls'), name='colleges'),
    path('colleges/', include('college_reviews.urls'), name='reviews'),
]
