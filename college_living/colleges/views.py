from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render

from colleges.models import College, CollegeClass, Professor, Dorms, ResidentialArea


# TODO: fix requests to ensure they're unique for colleges
# TODO: store college in cache
# TODO; professor slugs?

def college_home(request, college_name, country='US'):
    """
    College Name
        Residential Hall
                Dorms
        Other Dorms
    """
    college = College.approved_colleges.get(slug=college_name, country=country)
    return render(request, 'colleges/CollegeHome.html', {'college': college})

"""
    get all the dorms for the college
"""
def college_on_campus_living(request, college_name, country='US'):
    college = College.approved_colleges.get(slug=college_name, country=country)
    dorms = []
    for dorm in college.dorms_set.order_by('dorm_name'):
        dorms.append(dorm.dorm_name)

    return render(request,'colleges/CollegeDorms.html', {'college': college, 'dorms': dorms})

"""
    get all classes for the college
"""
def college_classes(request, college_name, country='US'):
    college = College.approved_colleges.get(slug=college_name, country=country)
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


def edit_college(request, college_name, country='US'):
    pass
"""
moderation view
    1. views for residential halls, dorms, etc.
    2. list all of moderation objects for them
    3. ability for user to approve/disapprove
    only if user is in group view
    
    /moderation
"""
def get_moderated_dorms(request, college_name, country='US'):
    try:
        college = College.approved_colleges.get(slug=college_name, country=country)
        Dorms.unmoderated_objects.filter(college=college)
    except College.DoesNotExist:
        raise Http404('College does not exist')
    return HttpResponse('<h1>Page was found</h1>')


def get_moderated_resAreas(request, college_name, country='US'):
    pass


# get list of colleges professors
def get_all_college_professors(request, college_name, country='US'):
    college = College.approved_colleges.get(slug=college_name, country=country)
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
def get_college_professor(request, college_name, professor_id, professor_slug, country='US'):
    try:
        professor = Professor.objects.get(id=professor_id)
        college = College.approved_colleges.get(email_domain=professor.college_id)
    except Professor.DoesNotExist:
        # TODO: redirect and add informative message
        return Http404('Professor Does not exist')
    return render(request, 'professors/ProfessorProfile.html',
                  {'college': professor.college_id, 'professor': professor})
