from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from colleges.models import College, CollegeClass, Professor, Dorms, ResidentialArea


# TODO: fix requests to ensure they're unique for colleges
# TODO: store college in cache
# TODO; professor slugs?

def college_home(request, college_id, college_slug=None):
    """
    College Name
        Residential Hall
                Dorms
        Other Dorms
    """
    college = College.approved_colleges.get(id=college_id)
    return render(request, 'colleges/CollegeHome.html', {'college': college})

"""
    get all the dorms for the college
"""


def college_on_campus_living(request, college_id, college_slug=None):
    college = College.approved_colleges.get(id=college_id)
    dorms = []
    for dorm in college.dorms_set.order_by('dorm_name'):
        dorms.append(dorm.dorm_name)

    return render(request, 'colleges/CollegeDorms.html', {'college': college, 'dorms': dorms})

"""
    get all classes for the college
"""


def college_classes(request, college_id, college_slug=None):
    college = College.approved_colleges.get(id=college_id)
    course_objects = CollegeClass.objects.filter(college=college)
    course_names = []
    # TODO: try to make only one query work with javascript
    for course in course_objects:
        course_names.append(course.class_name)

    return render(
        request, 'colleges/CollegeCourses.html',
        {
            'college': college,
            'course_objects': course_objects,
            'course_names': course_names
        }
    )

"""
    get the page for a given class
"""


def college_class(request, college_id, course_id, college_slug=None):
    return redirect('reviews:class_review_home', college_id=college_id, college_slug=college_slug, course_id=course_id)


def edit_college(request, college_id, college_slug=None):
    pass
"""
moderation view
    1. views for residential halls, dorms, etc.
    2. list all of moderation objects for them
    3. ability for user to approve/disapprove
    only if user is in group view
    
    /moderation
"""


def get_moderated_dorms(request, college_id, college_slug=None):
    try:
        college = College.approved_colleges.get(id=college_id)
        Dorms.unmoderated_objects.filter(college=college)
    except College.DoesNotExist:
        raise Http404('College does not exist')
    return HttpResponse('<h1>Page was found</h1>')


def get_moderated_resAreas(request, college_id, college_slug=None):
    pass


# get list of colleges professors
def get_all_college_professors(request, college_id, college_slug=None):
    college = College.approved_colleges.get(id=college_id)
    professors = Professor.objects.filter(college=college)
    return render(
        request,
        'professors/ProfessorsHome.html',
        {
            'college': college,
            'professors': professors
        }
    )


# gets the specific professor
# TODO: change to get_object_or_404
def get_college_professor(request, college_id, professor_id, college_slug=None, professor_slug=None):
    try:
        professor = Professor.objects.get(id=professor_id)
        college = College.approved_colleges.get(id=college_id)
        statistics = professor.get_statistics()
    except Professor.DoesNotExist:
        # TODO: redirect and add informative message
        return Http404('Professor Does not exist')
    return render(
        request, 'professors/ProfessorProfile.html',
        {
            'college': professor.college_id,
            'professor': professor,
            'statistics': statistics
        }
    )
