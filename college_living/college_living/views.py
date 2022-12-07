from django.shortcuts import render

<<<<<<< Updated upstream

# home page of the application
def home(request):
    return render(request, 'HomePage.html')
=======
from colleges.models import College


# home page of the application
def home(request):
    college = College.approved_colleges.all()[:3]
    return render(request, 'HomePage.html', {'colleges': college})
>>>>>>> Stashed changes
