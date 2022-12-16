from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from .forms import AddCourseReviewForm
from .models import CourseReview

from users.models import User

from colleges.models import CollegeClass


# Create your views here.

def create_course_review(request, college_name, course_id):
    if request.POST:
        form = AddCourseReviewForm(request.POST)
        if request.user.is_authenticated and form.is_valid():
            user = User.objects.get(pk=request.user.id)
            course = CollegeClass.objects.get(pk=course_id)
            if CourseReview.objects.filter(user=user, course=course).count() == 0:
                CourseReview.objects.create(
                    course=course,
                    user=user,
                    comment=form.cleaned_data['comment'],
                    test_heavy=form.cleaned_data['test_heavy'],
                    usefulness=form.cleaned_data['usefulness'],
                    theoretical=form.cleaned_data['theoretical'],
                    take_again=form.cleaned_data['take_again'],
                    term=form.cleaned_data['term']
                )
        return redirect(list_course_review, college_name=college_name, course_id=course_id)
    return render(request, 'course_reviews/AddCourseReview.html', {'form': AddCourseReviewForm})


def list_course_review(request, college_name, course_id):
    course = CollegeClass.objects.get(pk=course_id)
    reviews = CourseReview.objects.filter(course=course)
    content = {
        'reviews': reviews,
        'course': course
    }
    return render(request, 'course_reviews/CourseReviewHome.html', content)


def edit_course_review(request, college_name, course_id, course_review_id):
    review = CourseReview.objects.get(pk=course_review_id, course_id=course_id)
    return render(request, 'course_reviews/AddCourseReview.html', {'form': AddCourseReviewForm()})


def delete_course_review(request, college_name, course_id, course_review_id):
    review = CourseReview.objects.get(pk=course_review_id, course_id=course_id)
    review.delete()
    reviews = CourseReview.objects.filter(course_id=course_id)
    return render(request, 'course_reviews/CourseReviewHome.html', {'reviews': reviews})

