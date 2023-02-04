from django.http import HttpResponse
from django.shortcuts import render

from colleges.models import College, Dorms


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
        pass
    return HttpResponse('<h1>Page was found</h1>')


def get_moderated_resAreas(request, college_id, college_slug=None):
    pass

