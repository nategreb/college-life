from django.db import models
from slugify import slugify

from .departments import Department
from .colleges import College

"""
    One to Many relation of Colleges to Courses
"""


class CollegeCourse(models.Model):
    class Meta:
        # can have same course at different levels
        constraints = [
            models.UniqueConstraint(fields=['college', 'department', 'course_name', 'course_id'],
                                    name='college_course_alt_key'),
            models.UniqueConstraint(fields=['course_id'],
                                    name='secondary_course_id_key')

        ]

    college = models.ForeignKey(
        College,
        on_delete=models.CASCADE
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT
        # don't allow deletion of department if referenced
    )
    course_id = models.CharField(
        max_length=15,
        verbose_name='unique ID of the course'
    )
    course_name = models.CharField(
        max_length=90,
        verbose_name='name of course'
    )
    slug = models.SlugField(max_length=90, blank=True, null=False)

    def __str__(self):
        return self.course_name

    # add slug by converting white spaces to hyphens
    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.course_name}')
        # call full clean to validate
        self.full_clean()
        super().save(*args, **kwargs)


"""
 SemesterYear are the possible semesters and year at a university
"""


class SemesterYear(models.Model):
    term = models.CharField(
        max_length=11,
    )

    def __str__(self):
        return self.term
