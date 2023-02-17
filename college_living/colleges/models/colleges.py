from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.template.defaultfilters import slugify

from .departments import Department


class AllCollegesManager(models.Manager):
    # get college based on email
    def get_college(self, email):
        """
            API used:
                only contains the [domain] portion. For example, an email address might be 
                no cities
                two formats: [user]@[department].[domain] or [user]@[domain]
        """
        college = None

        try:
            validate_email(email)
        except ValidationError:
            print('invalid email')
            return college

        email = email.split('@')[1]

        # get the substring after the first domain
        without_department = email.split('.', 1)[1]

        # query based on equality of email with and without_department
        try:
            college = College.all_colleges.get(email_domain=email)
        except College.DoesNotExist:
            try:
                college = College.all_colleges.get(email_domain=without_department)
            except College.DoesNotExist:
                print('college with this domain does not exist')
        return college


# college manager for only approved colleges
class ApprovedCollegeManager(AllCollegesManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_approved=True)


# Create your models here.
class College(models.Model):
    class Meta:
        # https://github.com/hipo/university-domains-list college names are unique
        constraints = [
            models.UniqueConstraint(fields=['college_name', 'state_province', 'country'],
                                    name='college_alt_key'),
            models.UniqueConstraint(fields=['email_domain'],
                                    name='email_unique')
        ]

    email_domain = models.CharField(max_length=50)
    college_name = models.CharField(max_length=100, help_text='Please capitalize the name')
    state_province = models.CharField(max_length=20)
    country = models.CharField(max_length=2)  # alpha 2 code
    nickname = models.CharField(max_length=20, blank=True, null=True)
    date_created = models.DateField((""), auto_now=False, auto_now_add=True)
    date_modified = models.DateField((""), auto_now=True, auto_now_add=False)
    slug = models.SlugField(max_length=110, blank=True, null=False)
    is_approved = models.BooleanField(default=False, blank=True)

    departments = models.ManyToManyField(
        Department,
        help_text='Possible Departments in College',
        blank=True
    )

    # Managers
    all_colleges = AllCollegesManager()
    approved_colleges = ApprovedCollegeManager()

    # add slug by converting white spaces to hyphens
    def save(self, *args, **kwargs):
        self.slug = slugify(self.college_name)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.nickname:
            return self.nickname
        return self.college_name
