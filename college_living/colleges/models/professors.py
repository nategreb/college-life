from django.db import models

from .colleges import College
from .courses import CollegeClasses
from .departments import Department

 
class Professor(models.Model):
    class Meta: 
        constraints = [ 
            models.UniqueConstraint(fields=['college', 'department', 'first_name', 'last_name'], 
                                    name='class_subject_alt_key'),
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
        
    college         =   models.ForeignKey(
                            College,
                            on_delete=models.CASCADE
                        )        
    department      =   models.ForeignKey(
                            Department,
                            on_delete=models.PROTECT
                        )
    first_name      =   models.CharField(max_length = 20)
    last_name       =   models.CharField(max_length = 20)
    classes         =   models.ManyToManyField(CollegeClasses)

    grading_difficulty = models.PositiveSmallIntegerField(default=1)
    take_again = models.PositiveSmallIntegerField(default=1)
    teaching_quality = models.PositiveSmallIntegerField(default=1)
    personality = models.PositiveSmallIntegerField(default=1)