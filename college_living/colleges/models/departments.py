from django.db import models

"""
    Ex: Computer Science, Mathematics
"""


class Department(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Department Name',
        help_text='this is the name of the department',
        unique=True
    )

    def __str__(self):
        return self.name
