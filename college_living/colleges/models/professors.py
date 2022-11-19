from django.db import models

from .colleges import College
from .courses import CollegeClasses
from .departments import Department

 
class Professor(models.Model):
    class Meta: 
        constraints = [ 
            models.UniqueConstraint(fields=['college', 'department', 'first_name', 'last_name'], 
                                    name='class_subject_alt_key')        
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