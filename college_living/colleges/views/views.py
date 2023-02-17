from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.urls import reverse

from colleges.models import College, Dorms
from reviews.models import Review
from reviews.templatetags.review_tags import get_reviews
from colleges.forms import RequestCourseForm, RequestProfessorForm


def get_colleges(request):
    colleges = College.approved_colleges.all()
    # get the latest review
    rev = Review.objects.order_by('creation_date').last()
    obj = None
    if rev:
        ct = ContentType.objects.get(id=rev.content_type.id)
        # get object reviewed
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


@login_required
def request_add_course(request, college_id, college_slug=None):
    college = get_object_or_404(College, id=college_id)
    context = {'college': college, 'content_type': 'course'}
    if request.method == 'POST':
        form = RequestCourseForm(request.POST)
        if form.is_valid():
            if request.user.college != form.cleaned_data['college']:
                messages.add_message(request, messages.ERROR, 'You can only request to add objects to your school.')
            else:
                messages.add_message(request, messages.INFO, 'Request submitted')
                form.save()
                return redirect(reverse('home'))
    else:
        form = RequestCourseForm()
        form.initial['college'] = college
    context.update({'form': form})
    return render(request, 'colleges/RequestAddObject.html', context=context)


@login_required()
def request_add_professor(request, college_id, college_slug=None):
    college = get_object_or_404(College, id=college_id)
    context = {'college': college, 'content_type': 'professor'}
    if request.method == 'POST':
        form = RequestProfessorForm(request.POST)
        if form.is_valid():
            if request.user.college != form.cleaned_data['college']:
                messages.add_message(request, messages.ERROR, 'You can only request to add objects to your school.')
            else:
                messages.add_message(request, messages.INFO, 'Request submitted')
                form.save()
                return redirect(reverse('home'))
    else:
        form = RequestProfessorForm()

    form.initial['college'] = college
    context.update({'form': form})
    return render(request, 'colleges/RequestAddObject.html', context=context)
