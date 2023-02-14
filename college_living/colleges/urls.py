from django.urls import path, include
from .views import views, professor_view, courses_view, search_view

app_name = 'colleges'

urlpatterns = [
    path('', views.get_colleges, name='all_colleges'),
    path('<int:college_id>/<slug:college_slug>/', include([
        path('', views.college_home, name='college_home'),
        path('dorms/', views.college_on_campus_living, name='dorms'),

        # moderation links
        path('edit/', views.edit_college),
        path('edit/residential-areas/', views.get_moderated_resAreas),
        path('edit/dorms', views.get_moderated_dorms),

        # professors
        # path('professors/', professor_view.get_all_college_professors, name='professors'),
        path('professors/', search_view.ProfessorSearchView.as_view(), name='professors'),
        path('professor/<int:professor_id>/', professor_view.get_college_professor, name='professor'),
        path('professor/<int:professor_id>/<slug:professor_slug>/', professor_view.get_college_professor,
             name='professor'),

        # courses
        path('courses/', search_view.CoursesSearchView.as_view(), name='courses'),
        path('courses/<int:course_id>/', courses_view.college_course, name='course'),
        path('courses/<int:course_id>/<slug:course_slug>/', courses_view.college_course, name='course'),

        # search
        path('professors/search/', search_view.ProfessorSearchView.as_view(), name='professor_search'),
        path('professors/search/results/', search_view.ProfessorSearchView.as_view(), name='search_results'),

        path('courses/search/', search_view.CoursesSearchView.as_view(), name='course_search'),
        path('courses/search/results/', search_view.CoursesSearchView.as_view(), name='search_results'),

    ])),
]
