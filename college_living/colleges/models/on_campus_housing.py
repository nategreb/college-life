from django.db import models
from django.template.defaultfilters import slugify

from .colleges import College


class ResidentialArea(models.Model):
    class Meta: 
        constraints = [ 
            models.UniqueConstraint(fields=['college', 'res_hall_name'], 
                                    name='resArea_alt_key')        
        ]
    college     = models.ForeignKey(
                    College,
                    on_delete=models.CASCADE,
                    blank=True
                )
    res_hall_name   = models.CharField(max_length=100,
                                       help_text='Please capitalize the names',
                                       verbose_name='Residential Area Name'
                                       )
    date_created    = models.DateField((""), auto_now=False, auto_now_add=True)
    slug            = models.SlugField(max_length=110, blank=True, null=False)

    #add slug by converting white spaces to hyphens
    def save(self, *args, **kwargs):
        self.slug = slugify(self.res_hall_name)
        super().save(*args, **kwargs)

class Dorms(models.Model):
    class Meta: 
        constraints = [ 
            models.UniqueConstraint(fields=['college', 'dorm_name'], 
                                    name='dorms_alt_key')        
        ]
    residentialArea = models.ForeignKey(
                        ResidentialArea,
                        on_delete=models.CASCADE,
                        null=True,
                        blank=True,
                        help_text='Please capitalize the name'
                    )
    college         = models.ForeignKey(
                        College,
                        on_delete=models.CASCADE,
                        blank=True
                    )
    dorm_name       = models.CharField(max_length=100)
    date_created    = models.DateField((""), auto_now=False, auto_now_add=True)
    slug            = models.SlugField(max_length=110, blank=True, null=False)
    
    
    #add slug by converting white spaces to hyphens
    def save(self, *args, **kwargs):
        self.slug = slugify(self.dorm_name)
        super().save(*args, **kwargs)