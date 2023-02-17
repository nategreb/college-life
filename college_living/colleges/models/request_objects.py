from django.db import models

from colleges.models import CollegeCourse, College, Department


class RequestProfessor(models.Model):
    # Stores user requests to add specific professors
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['college', 'department', 'first_name', 'last_name'],
                name='request_prof_alt_key'
            )
        ]

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    courses = models.ManyToManyField(CollegeCourse, blank=True)

    college = models.ForeignKey(
        College,
        on_delete=models.CASCADE
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.college} - {self.department}'


class RequestCourse(models.Model):
    # Stores user requests to add specific courses
    class Meta:
        # can have same course at different levels
        constraints = [
            models.UniqueConstraint(fields=['college', 'department', 'course_name', 'course_id'],
                                    name='req_course_alt_key'),
            models.UniqueConstraint(fields=['course_id'],
                                    name='secondary_course_id_key_request_course')
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

    def __str__(self):
        return f'{self.course_name} - {self.college} - {self.department}'
