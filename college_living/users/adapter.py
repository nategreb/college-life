from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
import logging
from django.forms import ValidationError
from django.http import HttpResponse
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
                    Your college hasn\'t been approved yet. Please contact admin
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
            raise ImmediateHttpResponse(
                HttpResponse(
                    """
                        You are restricted from registering. 
                        Your college hasn\'t been approved yet. Please contact admin
                    """
                )
            )

        # sociallogin.connect(request, user)
