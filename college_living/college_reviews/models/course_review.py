from django.db import models

from colleges.models import CollegeClass
from users.models import User
from colleges.models.courses import SemesterYear


class CourseReview(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(
                name='check_review',
                check=models.Q(
                    test_heavy__range=(1, 5),
                    test_heavy__isnull=False,
                    usefulness__range=(1, 5),
                    usefulness__isnull=False,
                    theoretical__range=(1, 5),
                    theoretical__isnull=False,
                    take_again__range=(1, 5),
                    take_again__isnull=False
                )
            ),
            models.UniqueConstraint(
                name='user_course',
                fields=['user', 'course']
            )
        ]

    # Foreign key
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(CollegeClass, on_delete=models.CASCADE)
    term = models.ForeignKey(SemesterYear,on_delete=models.CASCADE)

    # date
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # review
    comment = models.CharField(max_length=160, blank=False)
    test_heavy = models.PositiveSmallIntegerField()
    usefulness = models.PositiveSmallIntegerField()
    theoretical = models.PositiveSmallIntegerField()
    take_again = models.PositiveSmallIntegerField()



