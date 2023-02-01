from django.db import models
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify

from .colleges import College
from .courses import CollegeClass
from .departments import Department


class Professor(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['college', 'department', 'first_name', 'last_name'],
                name='class_subject_alt_key'
            ),
            models.CheckConstraint(
                name='check_professor',
                check=models.Q(
                    grading_difficulty__range=(1, 5),
                    grading_difficulty__isnull=False,
                    take_again__range=(1, 5),
                    take_again__isnull=False,
                    teaching_quality__range=(1, 5),
                    teaching_quality__isnull=False,
                    personality__range=(1, 5),
                    personality__isnull=False
                )
            )
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

    # review fields
    grading_difficulty = models.PositiveSmallIntegerField(default=1)
    take_again = models.PositiveSmallIntegerField(default=1)
    teaching_quality = models.PositiveSmallIntegerField(default=1)
    personality = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    # url field
    slug = models.SlugField(max_length=40, blank=True, null=False)

    # add slug by converting white spaces to hyphens
    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.first_name} {self.last_name}')
        # call full clean to validate
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

    # calculates and scales the overall statistics of the professor
    def get_statistics(self):
        statistics = {
            'grading_difficulty': float(self.grading_difficulty / 5) * 100,
            'take_again': float(self.grading_difficulty / 5) * 100,
            'teaching_quality': float(self.teaching_quality / 5) * 100,
            'personality': float(self.personality / 5) * 100
        }
        overall = sum(statistics.values()) / len(statistics.keys())
        statistics['overall'] = overall
        return statistics
