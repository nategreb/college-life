"""
    get all classes for the college
"""
from allauth.exceptions import ImmediateHttpResponse
from django.core.checks import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from colleges.models import CollegeClass, College
from reviews.templatetags.review_tags import get_reviews


def college_classes(request, college_id, college_slug=None):
    college = College.approved_colleges.get(id=college_id)
    course_objects = CollegeClass.objects.filter(college=college)
    course_names = []
    # TODO: try to make only one query work with javascript
    for course in course_objects:
        course_names.append(course.class_name)

    return render(
        request, 'courses/CoursesHome.html',
        {
            'college': college,
            'course_objects': course_objects,
            'course_names': course_names
        }
    )


def college_class(request, college_id, course_id, college_slug=None):
    """
        get the profile for a given class
    """
    try:
        course = CollegeClass.objects.get(id=course_id)
        reviews = get_reviews(course)
        paginate = Paginator(reviews, 15)  # show 15 reviews per page
        page_number = request.GET.get('page')
        page_obj = paginate.get_page(page_number)
    except College.DoesNotExist:
        # add a one-time notification of the cause of failure
        messages.add_message(
            request, messages.ERROR,
            'This specific class doesn\'t exist'
        )
        raise ImmediateHttpResponse(HttpResponseRedirect(reverse('colleges:classes')))
    return render(
        request, 'courses/CourseProfile.html',
        {
            'course': course,
            'page_obj': page_obj
        }
    )
