"""URLs to run the tests."""
from django.urls import include, path
from django.contrib import admin
from django.views.generic import ListView

from ..models import Review

admin.autodiscover()

urlpatterns = [
    path(r'^reviews-listing/', ListView.as_view(model=Review),
         name='review_list'),
    path(r'^admin/', include(admin.site.urls)),
    path(r'^reviews/', include('reviews.urls')),
]
