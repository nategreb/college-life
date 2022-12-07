from django.urls import path, include
from . import views

app_name = 'colleges'

urlpatterns = [
    path('<slug:college_name>/', include([
        path('', views.college_home, name='college_home'),
        path('dorms/', views.college_on_campus_living, name='dorms'),
        path('classes/', views.college_classes, name='classes'),

        # moderation links
        path('edit/', views.edit_college),
        path('edit/residential-areas/', views.get_moderated_resAreas),
        path('edit/dorms', views.get_moderated_dorms),

        # professors
        path('professors', views.get_professors, name='professors'),
        path('professors/<int:professor_id>/<slug:professor_slug>', views.get_professor, name='professor'),
    ])),
]
