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
                name='check_professor_review',
                check=models.Q(
                    grading_difficulty__range=(1, 5),
                    grading_difficulty__isNulll=False,
                    take_again__range=(1, 5),
                    take_again__isNull=False,
                    teaching_quality__range=(1, 5),
                    teaching_quality__isNull=False,
                    personality__range=(1, 5),
                    personality__isNull=False
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

    grading_difficulty = models.PositiveSmallIntegerField()
    take_again = models.PositiveSmallIntegerField()
    teaching_quality = models.PositiveSmallIntegerField()
    personality = models.PositiveSmallIntegerField()