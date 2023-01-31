from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from .forms import AddCourseReviewForm, AddProfessorReviewForm
from .models import CourseReview, ProfessorReview

from users.models import User

from colleges.models import CollegeClass, Professor


# Create your views here.

def create_course_review(request, college_id, course_id, college_slug=None):
    if request.POST:
        form = AddCourseReviewForm(request.POST)
        if request.user.is_authenticated and form.is_valid():
            # TODO: pop up show error message
            user = User.objects.get(pk=request.user.id)
            course = CollegeClass.objects.get(pk=course_id)
            if CourseReview.objects.filter(user=user, course=course).count() == 0:
                # TODO: pop up show error message
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
        return redirect(
            'reviews:class_review_home',
            college_id=college_id,
            college_slug=college_slug,
            course_id=course_id
        )
    return render(request, 'course_reviews/AddCourseReview.html', {'form': AddCourseReviewForm})


def list_course_review(request, college_id, course_id, college_slug=None):
    course = CollegeClass.objects.get(pk=course_id)
    reviews = CourseReview.objects.filter(course=course)
    content = {
        'reviews': reviews,
        'course': course,
        'user': request.user.id,
        'college_id': college_id,
        'college_slug': college_slug
    }
    return render(request, 'course_reviews/CourseReviewHome.html', content)


def edit_course_review(request, college_name, course_id, course_review_id):
    try:
        review = CourseReview.objects.get(pk=course_review_id, course_id=course_id, user_id=request.user.id)
        form = AddCourseReviewForm(request.POST)
        if request.method == 'POST' and request.user.is_authenticated and form.is_valid():
            review.comment = form.cleaned_data['comment']
            review.test_heavy = form.cleaned_data['test_heavy']
            review.usefulness = form.cleaned_data['usefulness']
            review.theoretical = form.cleaned_data['theoretical']
            review.take_again = form.cleaned_data['take_again']
            review.term = form.cleaned_data['term']
            review.save()
            return redirect('reviews:class_review_home', college_name=college_name, course_id=course_id)
        return render(request, 'course_reviews/AddCourseReview.html', {'form': AddCourseReviewForm(instance=review)})
    except CourseReview.DoesNotExist:
        # TODO: pop up show error message
        return redirect('reviews:class_review_home', college_name=college_name, course_id=course_id)


def delete_course_review(request, college_name, course_id, course_review_id):
    try:
        review = CourseReview.objects.get(pk=course_review_id, course_id=course_id)
        review.delete()
    except CourseReview.DoesNotExist:
        # TODO: pop up show error message
        pass
    return redirect('reviews:class_review_home', college_name=college_name, course_id=course_id)


def create_professor_review(request, college_id, college_slug, professor_id):
    if request.POST:
        form = AddProfessorReviewForm(request.POST)
        if request.user.is_authenticated and form.is_valid():
            # TODO: pop up show error message
            user = User.objects.get(pk=request.user.id)
            professor = Professor.objects.get(pk=professor_id)
            if ProfessorReview.objects.filter(user=user, professor=professor).count() == 0:
                # TODO: pop up show error message
                ProfessorReview.objects.create(
                    professor=professor,
                    user=user,
                    comment=form.cleaned_data['comment'],
                    grading_difficulty=form.cleaned_data['grading_difficulty'],
                    take_again=form.cleaned_data['take_again'],
                    teaching_quality=form.cleaned_data['teaching_quality'],
                    personality=form.cleaned_data['personality'],
                    term=form.cleaned_data['term']
                )
        return redirect('reviews:professor_review_home', college_name=college_name, professor_id=professor_id)
    return render(request, 'professor_reviews/AddProfessorReview.html', {'form': AddProfessorReviewForm})


def list_professor_review(request, college_id, college_name, professor_id):
    professor = Professor.objects.get(pk=professor_id)
    reviews = ProfessorReview.objects.filter(professor=professor)
    content = {
        'reviews': reviews,
        'professor': professor,
        'user': request.user.id,
        'college': college_name
    }
    return render(request, 'professor_reviews/ProfessorReviewHome.html', content)


def edit_professor_review(request, college_id, college_name, professor_id, professor_review_id):
    try:
        review = ProfessorReview.objects.get(pk=professor_review_id, professor_id=professor_id, user_id=request.user.id)
        form = AddProfessorReviewForm(request.POST)
        if request.method == 'POST' and request.user.is_authenticated and form.is_valid():
            review.comment = form.cleaned_data['comment']
            review.grading_difficulty = form.cleaned_data['grading_difficulty']
            review.take_again = form.cleaned_data['take_again']
            review.teaching_quality = form.cleaned_data['teaching_quality']
            review.personality = form.cleaned_data['personality']
            review.term = form.cleaned_data['term']
            review.save()
            return redirect('reviews:professor_review_home', college_name=college_name, professor_id=professor_id)
        return render(request, 'professor_reviews/AddProfessorReview.html',
                      {'form': AddProfessorReviewForm(instance=review)})
    except ProfessorReview.DoesNotExist:
        # TODO: pop up show error message
        return redirect('reviews:professor_review_home', college_name=college_name, professor_id=professor_id)


def delete_professor_review(request, college_id, college_name, professor_id, professor_review_id):
    try:
        review = ProfessorReview.objects.get(pk=professor_review_id, professor_id=professor_id)
        review.delete()
    except ProfessorReview.DoesNotExist:
        # TODO: pop up show error message
        pass
    return redirect('reviews:professor_review_home', college_name=college_name, professor_id=professor_id)
