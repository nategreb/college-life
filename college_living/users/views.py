from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import EmailMultiAlternatives

from college_living.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm
from django.template.loader import get_template

from colleges.models import College


def get_user_profile(request):
    college = College.all_colleges.get(id=request.user.college_id)
    return render(request, 'ProfileHome.html', {'college': college})


########### register here #####################################
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            ######################### mail system ####################################
            htmly = get_template('Email.html')
            d = {'username': username}
            subject, from_email, to = 'welcome', EMAIL_HOST_USER, email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            ##################################################################
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'Register.html', {'form': form, 'title': 'reqister here'})


################ login forms###################################################
def login(request):
    if request.method == 'POST':

        # AuthenticationForm_can_also_be_used__

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' wecome {username} !!')
            return redirect('index')
        else:
            messages.info(request, f'account done not exit plz sign in')
    form = AuthenticationForm()
    return render(request, 'Login.html', {'form': form, 'title': 'log in'})

# https://www.geeksforgeeks.org/django-sign-up-and-login-with-confirmation-email-python/
# CONTAINS ALL THE HTML FILES NEEDED FOR THE ABOVE VIEWS
