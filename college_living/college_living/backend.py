from django.contrib.auth.backends import BaseBackend
from django.core.validators import validate_email
from django.forms import ValidationError
from users.models import User

"""
Custom authentication backend for Users
"""
class EmailOrUsernameModelBackend(object):
    def authenticate(self, request, username=None, password=None):
        if self.is_email(username):
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    #return boolean based on email validation
    def is_email(self, email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False
