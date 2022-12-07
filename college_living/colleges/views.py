from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render

from colleges.models import College, Dorms, ResidentialArea


def college_home(request, college_name, country='US'):
    """
    College Name
        Residential Hall
                Dorms
        Other Dorms
    """
    college = College.approved_colleges.get(slug=college_name, country=country)
    return render(request,'colleges/CollegeHome.html', {'college': college})

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
    classes = []



    return render(request, 'colleges/CollegeClasses.html', {'college': college, 'classes': classes})


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