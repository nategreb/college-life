from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', TemplateView.as_view(template_name='About.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='Contact.html'), name='contact'),

    # third party
    path('accounts/', include('allauth.urls')),
    path('reviews/', include('reviews.urls')),

    # apps
    path('', home, name='home'),
    path('colleges/', include('colleges.urls'), name='colleges'),
    path('users/', include('users.urls'), name='users'),

    # debugging
    path('__debug__/', include('debug_toolbar.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]
