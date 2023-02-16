from django.shortcuts import render, redirect
from django.urls import reverse

from colleges.models import College


# home page of the application
def home(request):
    if request.user.is_authenticated and request.user.college:
        try:
            College.approved_colleges.get(id=request.user.college.id)
            return redirect(reverse('colleges:college_home',
                                    kwargs={
                                        'college_id': request.user.college.id,
                                        'college_slug': request.user.college.slug,
                                    }
                                    )
                            )
        except College.DoesNotExist:
            pass
    colleges = College.approved_colleges.all()
    return render(
        request,
        'HomePage.html',
        {'colleges': colleges})
