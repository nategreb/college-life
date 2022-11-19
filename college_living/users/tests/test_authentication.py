from django.test import TestCase
from django.contrib.auth import authenticate
from users.models import User
    

class TestAuthenticationUser(TestCase):
    def setUp(self):
        User.objects.create_user(
            'test',
            'test@test.edu',
            'testing123'
        )
        User.objects.create_user(
            'nategreb',
            'ngrebelsky@umass.edu',
            'testing123'
        )

    #test custom backend with login email
    def test_email_login(self):
        self.assertIsNotNone(
            authenticate(
                username='test@test.edu',
                password='testing123'
            )
        )
    
    
    #test custom backend with login username
    def test_username_login(self):
        self.assertIsNotNone(
            authenticate(
                username='test@test.edu',
                password='testing123'
            )
        )
        
    #test custom backend with login email
    def test(self):
        self.assertIsNotNone(
            authenticate(
                username='ngrebelsky@umass.edu',
                password='testing123'
            )
        )
        
    #test non existing user
    def test_non_existing_user(self):
        self.assertIsNone(
            authenticate(
                username='bob@umass.edu',
                password='testing123'
            )
        )
