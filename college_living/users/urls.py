from django.urls import path, include
import users.views as views

urlpatterns = [
    path('profile/', views.get_user_profile, name='profile'),
]
