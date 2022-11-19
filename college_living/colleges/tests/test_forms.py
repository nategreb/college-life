from django.test import TestCase
from colleges.forms import NewResidentialAreaForm, NewDorm
from colleges.models import College, ResidentialArea

class TestResAreaForm(TestCase):
    #initialize test database with data
    def setUp(self):
        self.college = College.all_colleges.create(
                            email_domain = 'test.edu',
                            college_name = 'University Testing',
                            country = 'US',
                            is_approved = True
                        )
    
    def test_valid_new_area(self):
        data = {
            'res_hall_name': 'testing123'
        }
        form = NewResidentialAreaForm(data)
        self.assertTrue(form.is_valid())

class TestDormForms(TestCase):
    #initialize test database with data
    def setUp(self):
        self.college = College.all_colleges.create(
                            email_domain = 'test.edu',
                            college_name = 'University Testing',
                            country = 'US',
                            is_approved = True
                        )
        self.res_hall = ResidentialArea.objects.create(
            college = self.college,
            res_hall_name = 'testing area'            
        )
        
    #test form is valid with no res halls
    def test_valid_new_dorm_no_res_hall(self):
        data = {
            'dorm_name': 'test123'            
        }
        form = NewDorm(data)
        self.assertTrue(form.is_valid())
        
    #test form is valid with res hall
    def test_valid_new_dorm_with_res_hall(self):
        data = {
            'dorm_name': 'test123',
            'residentialArea': 'res_hall123'
        }
        form = NewDorm(data)
        self.assertTrue(form.is_valid())