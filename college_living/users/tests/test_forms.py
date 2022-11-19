from django.test import TestCase
from users.models import User
from colleges.models import College
from users.forms import UserRegisterForm

class UserRegistrationForm(TestCase):
    def setUp(self):
        College.all_colleges.create(
            email_domain = 'test.edu',
            college_name = 'University Testing',
            country = 'US',
            is_approved = True
        )
    
    #test passwords results in ValidationError
    def test_mismatched_passwords(self):
        #with self.assertRaises(ValidationError):
        data = {
            'email': 'nate.greb@test.edu',
            'username': 'nategreb',
            'confirm_password': '1',
            'password': '123'}
        self.assertFalse(UserRegisterForm(data).is_valid())
    
    #test passwords match result valid form
    def test_matching_passwords(self):
        data = {
                'email': 'nate.greb@test.edu',
                'username': 'nategreb',
                'confirm_password': '123',
                'password': '123'}
        form = UserRegisterForm(data)
        self.assertTrue(form.is_valid())
    
    #test invalid email input
    def test_invalid_email(self):
        #with self.assertRaises(ValidationError):
        data = {
            'email': 'nate.greb',
            'username': 'nategreb',
            'confirm_password': '123',
            'password': '123'}
        self.assertFalse(UserRegisterForm(data).is_valid())
    
    #test valid email input
    def test_valid_email(self):
        data = {
                'email': 'nate.greb@test.edu',
                'username': 'nategreb',
                'confirm_password': '123',
                'password': '123'}
        form = UserRegisterForm(data)
        self.assertTrue(form.is_valid())  
    
    #test invalid username 
    def test_invalid_username(self):
        data = {
            'email': 'nate.greb@test.edu',
            'username': '',
            'confirm_password': '123',
            'password': '123'}
        self.assertFalse(UserRegisterForm(data).is_valid())
        
    #test create user instance with valid form
    def test_valid_user_creation(self):        
        data = {
            'email': 'nate.greb@test.edu',
            'username': 'nategreb',
            'confirm_password': '123',
            'password': '123'}
        user = UserRegisterForm(data).save(commit=False)
        self.assertIsInstance(user, User)
        
    #test save user form with existing college in email
    def test_valid_college(self):
        data = {
            'email': 'nate.greb@test.edu',
            'username': 'nategreb',
            'confirm_password': '123',
            'password': '123'}
        user = UserRegisterForm(data).save(commit=False)
        college = College.all_colleges.get(email_domain='test.edu')        
        #make sure save from form is getting college
        self.assertEquals(user.college, college)
        
    #test save user form with non-existing college in email
    def test_non_valid_college(self):
        data = {
            'email': 'nate.greb@bob.edu',
            'username': 'nategreb',
            'confirm_password': '123',
            'password': '123'}
        user = UserRegisterForm(data).save(commit=False)   
        self.assertIsNone(user.college)