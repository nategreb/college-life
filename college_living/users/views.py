from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from colleges.models import College
from reviews.models import Review


def get_user_profile(request):
    college = College.all_colleges.get(id=request.user.college_id)
    reviews = Review.objects.filter(user_id=request.user.id)
    paginate = Paginator(reviews, 15)
    page_number = request.GET.get('page')
    page_obj = paginate.get_page(page_number)
    return render(
        request,
        'users/ProfileHome.html',
        {'college': college, 'reviews': reviews, 'page_obj': page_obj}
    )
