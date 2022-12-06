from django.shortcuts import render


# home page of the application
def home(request):
    return render(request, 'HomePage.html')
