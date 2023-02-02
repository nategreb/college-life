from django.urls import path, include
from .views import views, professor_view, courses_view

app_name = 'colleges'

urlpatterns = [
    path('<int:college_id>/<slug:college_slug>/', include([
        path('', views.college_home, name='college_home'),
        path('dorms/', views.college_on_campus_living, name='dorms'),

        # moderation links
        path('edit/', views.edit_college),
        path('edit/residential-areas/', views.get_moderated_resAreas),
        path('edit/dorms', views.get_moderated_dorms),

        # professors
        # path('professors/', professor_view.get_all_college_professors, name='professors'),
        path('professors/', professor_view.ProfessorSearchView.as_view(), name='professors'),
        path('professors/<int:professor_id>/', professor_view.get_college_professor, name='professor'),
        path('professors/<int:professor_id>/<slug:professor_slug>/', professor_view.get_college_professor,
             name='professor'),

        # classes
        path('classes/', courses_view.ClassesSearchView.as_view(), name='classes'),
        path('classes/<int:course_id>/', courses_view.college_class, name='class')
    ])),
]
