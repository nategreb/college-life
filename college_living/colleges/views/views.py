from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType

from colleges.models import College, Dorms
from reviews.models import Review
from reviews.templatetags.review_tags import get_reviews


def get_colleges(request):
    colleges = College.approved_colleges.all()
    # get the latest review
    rev = Review.objects.order_by('creation_date').last()
    if rev:
        ct = ContentType.objects.get(id=rev.content_type.id)
        obj = ct.get_object_for_this_type(id=rev.object_id)
    return render(
        request,
        'colleges/Colleges.html',
        {'colleges': colleges, 'review': rev, 'object': obj}
    )


def college_home(request, college_id, college_slug=None):
    college = College.approved_colleges.get(id=college_id)
    reviews = get_reviews(college)
    paginate = Paginator(reviews, 15)
    page_number = request.GET.get('page')
    page_obj = paginate.get_page(page_number)
    return render(request, 'colleges/CollegeHome.html', {'college': college, 'page_obj': page_obj})

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


