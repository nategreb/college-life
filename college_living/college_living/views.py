from django.shortcuts import render
from colleges.models import College

# home page of the application
def home(request):
    colleges = College.approved_colleges.all()
    return render(
        request,
        'HomePage.html',
        {'colleges': colleges})
