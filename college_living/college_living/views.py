from django.shortcuts import render
from colleges.models import College


# home page of the application
def home(request):
    college = College.approved_colleges.all()
    return render(request, 'HomePage.html', {'colleges': college})
