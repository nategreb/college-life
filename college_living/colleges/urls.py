from django.urls import path, include
from . import views

app_name = 'colleges'

urlpatterns = [
    path('<slug:college_name>/', include([
        path('', views.college_home, name='college_home'),
        path('dorms/', views.college_on_campus_living, name='dorms'),

        # moderation links
        path('edit/', views.edit_college),
        path('edit/residential-areas/', views.get_moderated_resAreas),
        path('edit/dorms', views.get_moderated_dorms),

        # professors
        path('professors/', views.get_all_college_professors, name='professors'),
        path('professors/<int:professor_id>/', views.get_college_professor, name='professor'),
        path('professors/<int:professor_id>/<slug:professor_slug>/', views.get_college_professor, name='professor'),

        # classes
        path('classes/', views.college_classes, name='classes'),
        path('classes/<int:id>/', views.college_class, name='class')
    ])),
]
