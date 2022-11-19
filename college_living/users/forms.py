from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import Group

from users.models import User
from colleges.models import College

from allauth.account.forms import SignupForm


#unbounded form to register users
class UserRegisterForm(ModelForm): 
    #want two password fields. One to verify they match
    email 			 = forms.EmailField(widget=forms.EmailInput()) 
    password		 = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    #clean the data
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        #assert the passwords match
        if password != confirm_password:
           raise forms.ValidationError(
                "password and confirm_password do not match",
                code='invalid'
            )
        return cleaned_data
    
    #custom save to align with User manager 
    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.college = College.all_colleges.get_college(self.cleaned_data['email'])
        if commit:
            user.save()
        return user

"""
    override SignUpForm to get college based on user's email    
"""
class CustomSignupForm(SignupForm):
    #TODO: call Users.models.create_user?
    def save(self, request):     
        user = super(CustomSignupForm, self).save(request)
        college = College.all_colleges.get_college(user.email)
        
        #add new user to Regular User group
        user.groups.add(Group.objects.get_or_create(name='Regular User')[0])        
        
        if college:
            user.college = college
            user.save()
        return user