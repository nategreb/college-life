from django.contrib.contenttypes.models import ContentType
from django.forms import ValidationError
from django.test import TestCase
from django.contrib.auth.models import Group, Permission
from users.models import User
from colleges.models import College


"""
1) test get college function
2) test college assignment
    - @[].[domain]
    - @domain
    
"""
class UserTestCase(TestCase):       
    def setUp(self):
        College.all_colleges.create(
            email_domain = 'test.edu',
            college_name = 'University Testing',
            country = 'US',
            is_approved = True
        )
        
        #add college Groups - same as in the Users migration 
        add_college_crud_to_user_groups()
    
    #test that create_admin creates a staff member
    def test_create_admin(self):
        user = User.objects.create_admin(
                'nategreb',
                'ngrebelsky@test.edu',
                'test123'
            )     
        self.assertTrue(user.is_staff)         
    
    #test that user can only be created with valid email
    def test_user_empty_email(self):        
        with self.assertRaises(ValueError):
            User.objects.create_user(
                    'nategreb',
                    ''                    
                )
    
    #test that user must have a valid email    
    def test_user_invalid_email(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                    'nategreb',
                    'bbb',
                    'test123'                  
                )
    
    #test that an 'edu' email is valid
    def test_new_user_simple_email_domain(self):
        user = User.objects.create_user(
                'nategreb',
                'ngrebelsky@test.edu',
                'test123'
            )
        college = College.all_colleges.get(email_domain='test.edu')        
        self.assertEquals(user.college, college)
    
    """
        Test that user is in the correct college
        even if they have a department in their email
    """
    def test_new_user_email_domain_and_department(self):
        user = User.objects.create_user(
                    'nategreb',
                    'ngrebelsky@cs.test.edu',
                    'test123'
                )
        college = College.all_colleges.get(email_domain='test.edu')        
        self.assertEquals(user.college, college)
        
    """
        Test that user can be created but with no 
        associated college        
    """
    def test_user_non_existing_college(self): 
        user = User.objects.create_user(
                    'nategreb',
                    'ngrebelsky@fake.edu',
                    'test123'
                )
        self.assertIsNone(user.college)
        
    #test regular user can become mod  
    def test_assigned_to_college_mod(self):
        user = User.objects.create_user(
                'nategreb',
                'ngrebelsky@test.edu',
                'test123'
            )
        user.make_college_mod()
        self.assertTrue(Group.objects.get(name='Mods') in user.groups.all())
     
    #test permissions are set for user with helper function   
    def test_mod_permissions(self):
        user = User.objects.create_user(
                'nategreb',
                'ngrebelsky@test.edu',
                'test123'
            )
        user.make_college_mod()
        self.assertEqual(len(user.groups.all()), 1)
        
    #test default create user is a regular user and is assigned only to this group
    def test_regular_group(self):
        user = User.objects.create_user(
                'nategreb',
                'ngrebelsky@test.edu',
                'test123'
            )        
        self.assertEqual(Group.objects.get(name='Regular User'), user.groups.all()[0])
        
    #test admin is in group admin
    def test_regular_group(self):
        user = User.objects.create_admin(
                'nategreb',
                'ngrebelsky@test.edu',
                'test123'
            )        
        self.assertTrue(Group.objects.get(name='Admin') in user.groups.all())
    
    
"""
The following helper functions is similar to the one used in one of the User data migrations to create
User Groups
"""
def add_college_crud_to_user_groups():
    #add the different groups users can be
    admins   = Group.objects.get_or_create(name='Admin')[0]
    mods     = Group.objects.get_or_create(name='Mods')[0]
    regulars = Group.objects.get_or_create(name='Regular User')[0]
    
    content_type = ContentType.objects.get_for_model(College)
    #add change permission for mods designated college 
    p1 = Permission.objects.create(
            name='Edit my college',
            codename='edit_my_college',
            content_type=content_type
        )
    p2 = Permission.objects.create(
            name='View College',
            codename='view_my_college',
            content_type=content_type
        )
    p3 = Permission.objects.create(
            name='Delete College',
            codename='delete_my_college',
            content_type=content_type
        )

    admins.permissions.add(p1,p2,p3)
    mods.permissions.add(p1,p2)
