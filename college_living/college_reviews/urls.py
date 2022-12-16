from django.urls import path, include

from . import views

app_name = 'reviews'

urlpatterns = [
    path('<slug:college_name>/classes/<int:course_id>/reviews/', include([
        path('', views.list_course_review, name='class_review_home'),
        path('create/', views.create_course_review, name='add_class_review'),
        path('<int:course_review_id>/edit/', views.edit_course_review, name='edit_class_review'),
        path('<int:course_review_id>/delete/', views.delete_course_review, name='delete_class_review'),
    ])),
]