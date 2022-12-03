from django.db import models

from .departments import Department
from .colleges import College


"""
    One to Many relation of Colleges to Courses
"""
class CollegeClasses(models.Model):
    class Meta: 
        #can have same course at different levels
        constraints = [
            models.CheckConstraint(
                name='check_course',
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
            models.UniqueConstraint(fields=['college', 'department', 'class_name', 'class_id'],
                                    name='college_classes_alt_key')        
        ]
    
    college     =   models.ForeignKey(
                        College,
                        on_delete=models.CASCADE
                    )            
    department  =   models.ForeignKey(
                        Department,
                        on_delete=models.PROTECT
                        #don't allow deletion of department if referenced
                    )
    class_id    =   models.CharField(
                        max_length=10,
                        verbose_name = 'unique ID of the course'                
                    )    
    class_name  =   models.CharField(
                        max_length = 75,
                        verbose_name = 'name of course'
                    )

    comment = models.CharField(max_length=160, blank=False)
    test_heavy = models.PositiveSmallIntegerField()
    usefulness = models.PositiveSmallIntegerField()
    theoretical = models.PositiveSmallIntegerField()
    take_again = models.PositiveSmallIntegerField()


