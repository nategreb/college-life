from django.db import IntegrityError
from django.test import TestCase
from colleges.models import (
    College,
    Department,
    CollegeClass,
)


class TestCourses(TestCase):
    def setUp(self):
        self.college = College.all_colleges.create(
            email_domain='test.edu',
            college_name='University Testing',
            state_province='test',
            country='US',
            is_approved=True,
        )

        self.compsci = Department.objects.create(name='Computer Science')
        self.history = Department.objects.create(name='History')

        self.college.departments.add(self.compsci, self.history)

        CollegeClass.objects.create(
            college=self.college,
            department=self.compsci,
            class_id='486',
            class_name='Machine Learning'
        )

        CollegeClass.objects.create(
            college=self.college,
            department=self.compsci,
            class_id='187',
            class_name='Data Structures'
        )

    # test college departments
    def test_college_departments(self):
        num_dep = self.college.departments.all().count()
        self.assertEqual(num_dep, 2)

    # test duplicate key: department
    def test_unique_subject_class(self):
        with self.assertRaises(IntegrityError):
            Department.object.create('Computer Science')

    # test duplicate key: class and subject
    def test_unique_subject_class(self):
        with self.assertRaises(IntegrityError):
            CollegeClass.objects.create(
                college=self.college,
                department=self.compsci,
                class_id='486',
                class_name='Machine Learning'
            )

    # get classes in subject
    def test_get_classes(self):
        num_courses = CollegeClass.objects.filter(department__name='Computer Science').count()
        self.assertEqual(num_courses, 2)

    # should be able to add class since its a different course number
    def test_class_with_diff_id(self):
        # same as in setUp but differs by class_id
        CollegeClass.objects.create(
            college=self.college,
            department=self.compsci,
            class_id='586',
            class_name='Machine Learning'
        )
        # get all computer science courses including added one from above
        num_courses = self.college.collegeclass_set.filter(
            department__name='Computer Science'
        ).count()
        self.assertEqual(num_courses, 3)

    # get Computer Science classes in college
    def test_get_classes_in_subject(self):
        num_courses = self.college.collegeclass_set.filter(
            department__name='Computer Science'
        ).count()
        self.assertEqual(num_courses, 2)

    # test getting all college classes
    def test_get_all_college_courses(self):
        CollegeClass.objects.create(
            college=self.college,
            department=self.history,
            class_id='586',
            class_name='Roman'
        )

        num_courses = self.college.collegeclass_set.all().count()
        self.assertEqual(num_courses, 3)

    # test deletion department. Nothing should happen
    def test_delete_department(self):
        with self.assertRaises(IntegrityError):
            Department.objects.get(name='Computer Science').delete()

    # test deletion college
    def test_delete_college(self):
        College.approved_colleges.get(email_domain='test.edu').delete()
        num_courses = CollegeClass.objects.all().count()
        self.assertEqual(num_courses, 0)
