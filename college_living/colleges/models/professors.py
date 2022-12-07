from django.db import models
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify

from .colleges import College
from .courses import CollegeClass
from .departments import Department


class Professor(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['college', 'department', 'first_name', 'last_name'],
                                    name='class_subject_alt_key')
        ]

    college = models.ForeignKey(
        College,
        on_delete=models.CASCADE
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    classes = models.ManyToManyField(CollegeClass)

    slug = models.SlugField(max_length=40, blank=True, null=False)

    # add slug by converting white spaces to hyphens
    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.first_name} {self.last_name}')
        # call full clean to validte
        self.full_clean()
        super().save(*args, **kwargs)

    # validate the models fields
    def clean(self):
        if not self.first_name:
            raise ValidationError({
                'first_name': ('First Name can\'t be empty'),
            })
        if not self.last_name:
            # field specific errors
            raise ValidationError({
                'last_name': ('Last Name can\'t be empty')
            })
