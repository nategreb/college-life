"""URLs for the reviews app."""
from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r'^(?P<pk>\d+)/delete/$', views.ReviewDeleteView.as_view(), name='review_delete'),
    re_path(r'^(?P<pk>\d+)/update/$', views.ReviewUpdateView.as_view(), name='review_update'),
    re_path(r'^(?P<pk>\d+)/$', views.ReviewDetailView.as_view(), name='review_detail'),
    re_path(r'^(?P<content_type>[-\w]+)/(?P<object_id>\d+)/create/$', views.ReviewCreateView.as_view(),
            name='review_create'),
]
