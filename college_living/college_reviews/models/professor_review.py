from django.db import models
from colleges.models import Department, Professor
from users.models import User
from colleges.models.courses import SemesterYear

class ProfessorReview(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(
                name='check_professor_review',
                check=models.Q(
                    grading_difficulty__range=(1, 5),
                    grading_difficulty__isnull=False,
                    take_again__range=(1, 5),
                    take_again__isnull=False,
                    teaching_quality__range=(1, 5),
                    teaching_quality__isnull=False,
                    personality__range=(1, 5),
                )
            )
        ]

    # Foreign key
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    professor = models.ForeignKey(
        Professor,
        on_delete=models.CASCADE
    )
    term = models.ForeignKey(SemesterYear, on_delete=models.CASCADE)

    # date
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # review
    comment = models.CharField(max_length=160, blank=False)

    grading_difficulty = models.PositiveSmallIntegerField()
    take_again = models.PositiveSmallIntegerField()
    teaching_quality = models.PositiveSmallIntegerField()
    personality = models.PositiveSmallIntegerField()




