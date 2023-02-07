from django.shortcuts import render
from colleges.models import College


# home page of the application
def home(request):
    return render(request, 'HomePage.html')
