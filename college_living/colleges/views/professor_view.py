from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import ListView

from colleges.models import College, Professor
from reviews.templatetags.review_tags import get_reviews


# get list of colleges professors
def get_all_college_professors(request, college_id, college_slug=None):
    college = College.approved_colleges.get(id=college_id)
    professors = Professor.objects.filter(college=college)
    paginate = Paginator(professors, 15)
    page_number = request.GET.get('page')
    page_obj = paginate.get_page(page_number)
    return render(
        request,
        'professors/ProfessorsHome.html',
        {
            'college': college,
            'professors': professors,
            'page_obj': page_obj
        }
    )


# gets the specific professor
# TODO: change to get_object_or_404
# TODO: optimize query if there are lots of reviews - breaking it up with caching
def get_college_professor(request, college_id, professor_id, college_slug=None, professor_slug=None):
    try:
        professor = Professor.objects.get(id=professor_id)
        reviews = get_reviews(professor)
        paginate = Paginator(reviews, 15)  # show 15 reviews per page
        page_number = request.GET.get('page')
        page_obj = paginate.get_page(page_number)
    except Professor.DoesNotExist:
        # TODO: redirect and add informative message
        return Http404('Professor Does not exist')
    return render(
        request, 'professors/ProfessorProfile.html',
        {
            'college': professor.college_id,
            'professor': professor,
            'page_obj': page_obj
        }
    )


