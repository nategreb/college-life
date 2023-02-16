from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
import logging
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse

from colleges.models import College


class RestrictEmailAdapter(DefaultAccountAdapter):
    """
        Only users with an email associated with an 
        approved colleges can sign up.
    """


    def clean_email(self, email):
        # get all approved email domains
        allowed_email_domains = College.approved_colleges.values_list('email_domain', flat=True)
        # clean up email and get the domain portion
        if email.lower().split('@')[1] not in allowed_email_domains:
            raise ValidationError(
                """
                    You are restricted from registering. 
                    Your college hasn\'t been approved yet. Please contact admin.
                """
            )
        return email
    # TODO: store email that tried to register to email them when college is approved


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    logger = logging.getLogger(__name__)

    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            return

        if 'email' not in sociallogin.account.extra_data:
            self.logger.info("'Email' field not in extra_data")
            raise ImmediateHttpResponse(HttpResponse('Email missing from social login - cannot verify user.'))

        email = sociallogin.account.extra_data['email'].lower()

        # email adapter to check email
        try:
            RestrictEmailAdapter().clean_email(email)
        except ValidationError:
            # add a one-time notification of the cause of failure
            messages.add_message(
                request, messages.ERROR,
                """                   
                   You are restricted from registering. You're either not using your school email
                   or your school hasn't been added yet. Please try again.                     
               """
            )
            raise ImmediateHttpResponse(HttpResponseRedirect(reverse('home')))

    def is_open_for_signup(self, request, socialaccount):
        return True

    def save_user(self, request, sociallogin, form=None):
        user = sociallogin.user
        # we know the email exists in approved colleges based on the pre_social_login
        user.college = College.approved_colleges.get_college(user.email)
        super(SocialAccountAdapter, self).save_user(request, sociallogin)
