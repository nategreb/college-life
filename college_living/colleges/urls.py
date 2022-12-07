from django.urls import path
from . import views

app_name = 'colleges'

urlpatterns = [
    path('<slug:college_name>/', views.college_home, name='college_home'),
    path('<slug:college_name>/dorms', views.college_on_campus_living, name='dorms'),
    path('<slug:college_name>/professors', views.college_home, name='professors'),
    path('<slug:college_name>/classes', views.college_classes, name='classes'),
    
    
    #moderation links
    path('<slug:college_name>/edit/', views.edit_college),
    path('<slug:college_name>/edit/residential-areas/', views.get_moderated_resAreas),
    path('<slug:college_name>/edit/dorms', views.get_moderated_dorms)
]