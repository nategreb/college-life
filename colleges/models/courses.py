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