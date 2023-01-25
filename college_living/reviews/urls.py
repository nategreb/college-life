"""URLs for the reviews app."""
from django.urls import path

from . import views

urlpatterns = [
    path(r'^(?P<pk>\d+)/delete/$',
         views.ReviewDeleteView.as_view(),
         name='review_delete'),
    path(r'^(?P<pk>\d+)/update/$',
         views.ReviewUpdateView.as_view(),
         name='review_update'),
    path(r'^(?P<pk>\d+)/$',
         views.ReviewDetailView.as_view(),
         name='review_detail'),
    path(r'^(?P<content_type>[-\w]+)/(?P<object_id>\d+)/create/$',
         views.ReviewCreateView.as_view(),
         name='review_create'),
]
