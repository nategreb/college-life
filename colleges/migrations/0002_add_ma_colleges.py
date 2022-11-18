# Generated by Django 4.0.4 on 2022-08-17 15:12

from django.db import migrations
from django.template.defaultfilters import slugify


def add_ma_colleges(apps, schema_editor):
    # We can't import the College model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    College = apps.get_model('colleges', 'College')
    
    for college in ma_colleges:
        #only make umass an approved college
        is_approved = True if college['domains'][0] == 'umass.edu' else False
        
        college =  College (
                email_domain = college['domains'][0], 
                college_name = college['name'],
                state_province = college['state_province'],
                country = college['alpha_two_code'],
                is_approved = is_approved
            )
        #can't call model methods in migration files
        college.slug = slugify(college.college_name)
        college.save()
        
   
def reverse_ma_colleges(apps, schema_editor):
    College = apps.get_model('colleges', 'College')
    
    for college in ma_colleges:
        College.all_colleges.get(
            email_domain = college['domains'][0]
        ).delete()
    

class Migration(migrations.Migration):

    dependencies = [
        ('colleges', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_ma_colleges, reverse_code=reverse_ma_colleges)
    ]


#following JSON is using http://universities.hipolabs.com/
#colleges can be in multiple cities. use state/province
ma_colleges = [
        {
            "domains": [
                "mit.edu"
            ],
            "alpha_two_code": "US",
            "country": "United States",
            "web_pages": [
                "http://web.mit.edu/"
            ],
            "name": "Massachusetts Institute of Technology",
            "state_province": "Massachusetts"
        },
        {
            "domains": [
                "massbay.edu"
            ],
            "alpha_two_code": "US",
            "country": "United States",
            "web_pages": [
                "http://www.massbay.edu"
            ],
            "name": "Massachusetts Bay Community College",
            "state_province": "Massachusetts"
        },
        {
            "domains": [
                "umb.edu"
            ],
            "alpha_two_code": "US",
            "country": "United States",
            "web_pages": [
                "https://www.umb.edu/"
            ],
            "name": "University of Massachusetts Boston",
            "state_province": "Massachusetts"
        },
        {
            "domains": [
                "umassd.edu"
            ],
            "alpha_two_code": "US",
            "country": "United States",
            "web_pages": [
                "http://www.umassd.edu/"
            ],
            "name": "University of Massachusetts Dartmouth",
            "state_province": "Massachusetts"
        },
        {
            "domains": [
                "umass.edu"
            ],
            "alpha_two_code": "US",
            "country": "United States",
            "web_pages": [
                "http://www.umass.edu/"
            ],
            "name": "University of Massachusetts Amherst",
            "state_province": "Massachusetts"
        },
        {
            "domains": [
                "uml.edu",
                "student.uml.edu"
            ],
            "alpha_two_code": "US",
            "country": "United States",
            "web_pages": [
                "http://www.uml.edu/"
            ],
            "name": "University of Massachusetts Lowell",
            "state_province": "Massachusetts"
        },
            {
            "domains": [
                "wpi.edu"
            ],
            "alpha_two_code": "US",
            "country": "United States",
            "web_pages": [
                "http://www.wpi.edu/"
            ],
            "name": "Worcester Polytechnic Institute",
            "state_province": "Massachusetts"
        },
            {
            "domains": [
                "bu.edu"
            ],
            "alpha_two_code": "US",
            "country": "United States",
            "web_pages": [
                "http://www.bu.edu/"
            ],
            "name": "Boston University",
            "state_province": "Massachusetts"
        },
        {
            "domains": [
                "bc.edu"
            ],
            "alpha_two_code": "US",
            "country": "United States",
            "web_pages": [
                "http://www.bc.edu/"
            ],
            "name": "Boston College",
            "state_province": "Massachusetts"
        }, 
        {
            "domains": [
                "harvard.edu"
            ],
            "alpha_two_code": "US",
            "country": "United States",
            "web_pages": [
                "http://www.harvard.edu/"
            ],
            "name": "Harvard University",
            "state_province": "Massachusetts"
        }
]   
