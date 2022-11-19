# from django.test import TestCase
# from django.core.exceptions import ObjectDoesNotExist
# from moderation.helpers import automoderate

# from colleges.models import College, ResidentialArea, Dorms
# from users.models import User


# class TestModeratorApproval(TestCase):
#     def setUp(self):
#         self.college = College.all_colleges.create(
#             email_domain = 'test.edu',
#             college_name = 'University Testing',
#             country = 'US',
#         )
        
#         #create user in group 'admin'
#         self.admin = User.objects.create_admin(
#             'nategreb',
#             'ngrebelsky@test.edu',
#             'test123'
#         )  
        
#         self.res_hall = ResidentialArea.objects.create(
#             college = self.college,
#             res_hall_name = 'testing area'            
#         )
    
#     """
#     test that residential areas aren't saved 
#     until after being appproved
#     """
#     def test_create_resHall_moderator(self):
#         self.assertTrue(len(ResidentialArea.objects.all()) == 0)        
#         self.res_hall.moderated_object.approve(by=None,
#                                            reason='create res hall')
#         self.assertTrue(len(ResidentialArea.objects.all()) == 1)        
        
        
#     """
#     test that dorms aren't saved until 
#     after being approved
#     """
#     def test_create_dorm_moderator(self):
#         dorm = Dorms.objects.create(
#             dorm_name = 'test',
#             college = self.college,
#             residentialArea = self.res_hall
#         )
#         with self.assertRaises(ObjectDoesNotExist):
#             Dorms.objects.get(pk=dorm.id)
            
#         dorm.moderated_object.approve(by=None,
#                                            reason='create dorm')
#         self.assertIsInstance(Dorms.objects.get(pk=dorm.id), Dorms)
        
#     """
#     test that dorms are automatically approved
#     if changed by a user 
#     """
#     def test_admin_approved(self):
#         dorm = Dorms.objects.create(
#             dorm_name = 'test2',
#             college = self.college,
#             residentialArea = self.res_hall
#         )
#         # dorm.moderated_object.approve(by=self.admin,
#         #                                    reason='create dorm')
        
#         # dorm.dorm_name = 'testAdminChange'
#         # dorm.save()
#         automoderate(dorm, self.admin)
#         self.assertIsInstance(Dorms.objects.get(pk=dorm.id), Dorms)
    
#     """
#     test that new object isn't stored into Dorms on creation
#     """
#     def test_creating_new_object(self):
#         dorm = Dorms.objects.create(
#             dorm_name = 'test3',
#             college = self.college,
#             residentialArea = self.res_hall
#         )
#         with self.assertRaises(ObjectDoesNotExist):
#             Dorms.objects.get(pk=dorm.id)
            
#     """
#         change by regular users isn't accepted right away    
#     """
#     def test_create_dorm_reg_user(self):
#         #create user in group 'admin'
#         user = User.objects.create_user(
#             'regUser',
#             'regular@test.edu',
#             'test123'
#         )  
#         dorm = Dorms.objects.create(
#             dorm_name = 'testRegUser',
#             college = self.college,
#             residentialArea = self.res_hall
#         )
#         automoderate(dorm, user)
#         with self.assertRaises(ObjectDoesNotExist):
#             Dorms.objects.get(pk=dorm.id)
            
# class TestModeratorQueries(TestCase):
#     def setUp(self):
#         self.college = College.all_colleges.create(
#                 email_domain = 'test.edu',
#                 college_name = 'University Testing',
#                 country = 'US'
#             )
        
#         self.res_hall = ResidentialArea.objects.create(
#             college = self.college,
#             res_hall_name = 'testing area'            
#         )
        
#         self.admin = User.objects.create_admin(
#                     'nategreb',
#                     'ngrebelsky@test.edu',
#                     'test123'
#                 )  
#         #create a mix of dorms with/out Res Area
#         for i in range(5):
#             res_hall = self.res_hall
#             if i > 2:
#                 res_hall = None 
#             dorm = Dorms.objects.create(
#                 dorm_name = 'test'+str(i),
#                 college = self.college,
#                 residentialArea = res_hall
#             )
#             automoderate(dorm, self.admin)        
            
#         #approve residential area
#         automoderate(self.res_hall, self.admin)
        
#     """
#     test all specific College dorms added to moderation.
#     this should only return dorms created in the constructor.
#     """
#     def test_moderator_query_dorms(self):
#         diffcollege = College.all_colleges.create(
#                         email_domain = 'diff.edu',
#                         college_name = 'University different',
#                         country = 'US',
#                     )
#         dorm = Dorms.objects.create(
#             dorm_name = 'testdiffcollege',
#             college = diffcollege
#         )
#         automoderate(dorm, self.admin)        
#         self.assertEqual(len(Dorms.unmoderated_objects.filter(college=self.college)), 5)
        
#     #test all College resAreas added to moderation
#     def test_moderator_query_res_halls(self):
#         self.assertEqual(len(ResidentialArea.unmoderated_objects.filter(college=self.college)), 1)
        
#     """
#     Test Dorms approval without ResArea being approved
#     Test should still return all the dorms that are approved based
#     on the moderation app.
#     """    
#     def test_dorm_without_resArea_approved(self):
#         diffcollege = College.all_colleges.create(
#                         email_domain = 'unique.edu',
#                         college_name = 'University',
#                         country = 'US',
#                     )
#         res_hall = ResidentialArea.objects.create(
#             college = diffcollege,
#             res_hall_name = 'testing unique'            
#         )        
#         dorm = Dorms.objects.create(
#             dorm_name = 'testNoResAreaApproved',
#             college = diffcollege,
#             residentialArea = res_hall
#         )
#         automoderate(dorm, self.admin) 
#         self.assertEqual(len(Dorms.unmoderated_objects.filter(college=diffcollege)), 1)
    