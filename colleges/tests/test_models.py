from django.db import IntegrityError
from django.test import TestCase
from users.models import User
from colleges.models import (
    College, 
    ResidentialArea, 
    Dorms, 
    Department,
    CollegeClasses,
    Professor
)


class TestCaseColleges(TestCase):
    #setup test database
    def setUp(self):
        College.all_colleges.create(
            email_domain = 'test.edu',
            college_name = 'University Testing',
            state_province = 'test',
            country = 'US',
            is_approved = True
        )
        
        College.all_colleges.create(
            email_domain = 'nonapproved.edu',
            college_name = 'University Not Approved',
            state_province = 'test',
            country = 'US'
        )
    
    #test college exists and query works
    def test_get_existing_college(self):
        email = 'test@test.edu'
        college = College.all_colleges.get_college(email)
        self.assertEqual(college.email_domain, 'test.edu')
    
    #test that this email domain doesn't exist
    def test_get_non_existing_college(self):
        email = 'test@non-existing.edu'
        college = College.all_colleges.get_college(email)
        self.assertIsNone(college)        
    
    #test that college is created with just the domain portion 'test.edu'
    def test_department_and_domain_get_college(self):
        email = 'test@med.test.edu'
        college = College.all_colleges.get_college(email)
        self.assertEquals(college.email_domain, 'test.edu') 
        
    #test all college manager with non approved college
    def test_get_non_approved_college(self):
        self.assertEqual(College.all_colleges.filter(email_domain='nonapproved.edu').count(),1)
    
    #test approved college managere with approved colleg
    def test_get_approved_college(self):
        self.assertEqual(College.approved_colleges.filter(email_domain='test.edu').count(),1)
        
    #test approved college managere with non approved college
    def test_get_non_approved_college_with_approved_manager(self):
        with self.assertRaises(College.DoesNotExist):
            College.approved_colleges.get(email_domain='nonapproved.edu')
        
class TestResidentialArea(TestCase):
    def setUp(self):
        self.college = College.all_colleges.create(
                email_domain = 'test.edu',
                college_name = 'University Testing',
                state_province = 'test',
                country = 'US',
                is_approved = True
            )
        res_hall = ResidentialArea.objects.create(
            college = self.college,
            res_hall_name = 'testing area'            
        )
    #test that creating residential area with just these fields is valid
    def test_secondary_key_valid(self):       
        area = ResidentialArea.objects.create(
            college = self.college,
            res_hall_name = 'testing diff'            
        )
        self.assertIsInstance(area, ResidentialArea)
        
class TestDorms(TestCase):
    def setUp(self):
        self.college = College.all_colleges.create(
                email_domain = 'test.edu',
                college_name = 'University Testing',
                state_province = 'test',
                country = 'US',
                is_approved = True
            )
        
        self.res_hall = ResidentialArea.objects.create(
            college = self.college,
            res_hall_name = 'testing area'            
        )
        
        self.admin = User.objects.create_admin(
                    'nategreb',
                    'ngrebelsky@test.edu',
                    'test123'
                )  
        #create a mix of dorms with/out Res Area
        for i in range(5):
            res_hall = self.res_hall
            if i > 2:
                res_hall = None 
            dorm = Dorms.objects.create(
                dorm_name = 'test'+str(i),
                college = self.college,
                residentialArea = res_hall
            )
        
    """
        Test that there are 2 dorms created in setup without res area
    """
    def test_no_res_hall(self):
        self.assertEqual(len(Dorms.objects.filter(college=self.college,residentialArea=None)),2)
    
    """
       Test that the above setup only created 3 dorms within the
       res__hall called 'testing area'
    """
    def test_with_res_hall(self):                
        self.assertEqual(len(self.res_hall.dorms_set.all()),3)
    
    """
        Test that the college created above has 5 dorms total
    """
    def test_college_dorms(self):
        self.assertEqual(len(self.college.dorms_set.all()),5)


class TestCourses(TestCase):
    def setUp(self):                
        self.college = College.all_colleges.create(
                email_domain = 'test.edu',
                college_name = 'University Testing',
                state_province = 'test',
                country = 'US',
                is_approved = True,                
            )
        
        self.compsci = Department.objects.create(name='Computer Science')
        self.history = Department.objects.create(name='History')
        
        self.college.departments.add(self.compsci, self.history)        
        
        CollegeClasses.objects.create(
            college=self.college, 
            department = self.compsci,
            class_id = '486',
            class_name = 'Machine Learning'
        )
        
        CollegeClasses.objects.create(
            college=self.college, 
            department = self.compsci,
            class_id = '187',
            class_name = 'Data Structures'
        )
           
    #test college departments
    def test_college_departments(self):
        num_dep = self.college.departments.all().count()
        self.assertEqual(num_dep, 2)
        
    #test duplicate key: department
    def test_unique_subject_class(self):
        with self.assertRaises(IntegrityError):
            Department.object.create('Computer Science')
    
    #test duplicate key: class and subject
    def test_unique_subject_class(self):
        with self.assertRaises(IntegrityError):
            CollegeClasses.objects.create(
                college=self.college, 
                department = self.compsci,
                class_id = '486',
                class_name = 'Machine Learning'
            )
    
    #get classes in subject
    def test_get_classes(self):
        num_courses = CollegeClasses.objects.filter(department__name='Computer Science').count()
        self.assertEqual(num_courses, 2)

    #should be able to add class since its a different course number
    def test_class_with_diff_id(self):               
        #same as in setUp but differs by class_id
        CollegeClasses.objects.create(
            college=self.college, 
            department = self.compsci,
            class_id = '586',
            class_name = 'Machine Learning'
        )
        #get all computer science courses including added one from above
        num_courses = self.college.collegeclasses_set.filter(
                        department__name = 'Computer Science'                                                
                    ).count()
        self.assertEqual(num_courses,3)
        
    #get Computer Science classes in college
    def test_get_classes_in_subject(self):
        num_courses = self.college.collegeclasses_set.filter(
                        department__name = 'Computer Science'                                                
                    ).count()       
        self.assertEqual(num_courses, 2)
        
    #test getting all college classes 
    def test_get_all_college_courses(self):
            CollegeClasses.objects.create(
                college=self.college, 
                department = self.history,
                class_id = '586',
                class_name = 'Roman'
            )
            
            num_courses = self.college.collegeclasses_set.all().count()
            self.assertEqual(num_courses, 3)
            
    #test deletion department. Nothing should happen
    def test_delete_department(self):
        with self.assertRaises(IntegrityError):
            Department.objects.get(name='Computer Science').delete()        
    
    #test deletion college
    def test_delete_college(self):
        College.approved_colleges.get(email_domain='test.edu').delete()
        num_courses = CollegeClasses.objects.all().count()
        self.assertEqual(num_courses, 0)
    
class TestProfessors(TestCase):
    def setUp(self):
        self.college = College.all_colleges.create(
                email_domain = 'test.edu',
                college_name = 'University Testing',
                state_province = 'test',
                country = 'US',
                is_approved = True,                
            )
          
        self.college2 = College.all_colleges.create(
            email_domain = 'test2.edu',
            college_name = 'test2',
            state_province = 'test',
            country = 'US',
            is_approved = True,                
        )
        
        self.compsci = Department.objects.create(name='Computer Science')
        
        self.class1 = CollegeClasses.objects.create(
                        college=self.college, 
                        department = self.compsci,
                        class_id = '486',
                        class_name = 'Machine Learning'
                    )   
        
        self.class2 = CollegeClasses.objects.create(
                        college=self.college, 
                        department = self.compsci,
                        class_id = '100',
                        class_name = 'Diffs'
                    ) 
         
    """
        Test querying different college's professors
    """  
    def test_get_diff_college_professors(self):
        #college
        prof1 = Professor.objects.create(
                        college = self.college,
                        department = self.compsci,
                        first_name =  'test',
                        last_name = 'test'                      
                    )
        #diff college
        prof2 = Professor.objects.create(
                        college = self.college2,
                        department = self.compsci,
                        first_name =  'test',
                        last_name = 'test'                      
                    )
        
        num_profs = Professor.objects.filter(college = self.college2).count()
        self.assertEqual(num_profs, 1)
    
        
    """
        test that correct associated professors for class are returned
    """
    def test_multiple_classes(self):
        for fname, lname in (('nate', 'greb'), ('ian', 'lewis'), ('alice', 'bob')):
            prof = Professor.objects.create(
                        college = self.college,
                        department = self.compsci,
                        first_name =  fname,
                        last_name = lname                       
                    )
            prof.classes.add(self.class1)
        
        #professor for diff class    
        diff =  Professor.objects.create(
                    college = self.college,
                    department = self.compsci,
                    first_name =  'test',
                    last_name = 'test'                      
                )
        
        diff.classes.add(self.class2)
        num_profs = Professor.classes.through.objects.filter(
                    collegeclasses_id = self.class1.id
                ).count()
        
        self.assertEqual(num_profs, 3)
    
    """
        get professors classes
    """
    def test_get_professors_classes(self):
        prof    =  Professor.objects.create(
                    college = self.college,
                    department = self.compsci,
                    first_name =  'test',
                    last_name = 'test'                      
                )
        
        prof.classes.add(self.class2)
        
        num_courses = prof.classes.count()
        self.assertEqual(num_courses, 1)
    
    """
        test professor with no courses
    """
    def test_no_courses(self):
        prof    =  Professor.objects.create(
                    college = self.college,
                    department = self.compsci,
                    first_name =  'test',
                    last_name = 'test'                      
                )
        
        self.assertEqual(prof.classes.count(), 0)
        
    """
        get professors from different departments
    """
    def test_diff_departments(self):
        for fname, lname in (('nate', 'greb'), ('ian', 'lewis'), ('alice', 'bob')):
            prof = Professor.objects.create(
                        college = self.college,
                        department = self.compsci,
                        first_name =  fname,
                        last_name = lname                       
                    )
            prof.classes.add(self.class1)
        
        history = Department.objects.create(name='History')
        
        #new professor in history department. differs from the above compsci courses
        Professor.objects.create(
            college = self.college,
            department = history,
            first_name =  'test',
            last_name = 'test'                      
        )
        
        num_profs = Professor.objects.filter(college=self.college, department=history).count()
        self.assertEqual(num_profs, 1)    
    
    """
        get all professors that share a course
    """
    def test_multiple_professors(self):
        for fname, lname in (('nate', 'greb'), ('ian', 'lewis'), ('alice', 'bob')):
            prof = Professor.objects.create(
                        college = self.college,
                        department = self.compsci,
                        first_name =  fname,
                        last_name = lname                       
                    )
            prof.classes.add(self.class1)
        
        #query many to many table directly
        num_profs = Professor.classes.through.objects.filter(
                        collegeclasses_id = self.class1.id
                    ).count()
        
        self.assertEqual(num_profs, 3)
        
    """
        test that department cant be deleted when referenced by professors
    """
    def test_delete_department(self):
        with self.assertRaises(IntegrityError):
            for fname, lname in (('nate', 'greb'), ('ian', 'lewis'), ('alice', 'bob')):
                prof = Professor.objects.create(
                            college = self.college,
                            department = self.compsci,
                            first_name =  fname,
                            last_name = lname                       
                        )
                prof.classes.add(self.class1)
            
            self.compsci.delete()
            
            num_profs = Professor.objects.count()
            
            self.assertEqual(num_profs, 3)