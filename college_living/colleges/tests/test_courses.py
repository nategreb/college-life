from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from colleges.models import (
    College,
    Department,
    CollegeCourse,
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

        CollegeCourse.objects.create(
            college=self.college,
            department=self.compsci,
            course_id='486',
            course_name='Machine Learning'
        )

        CollegeCourse.objects.create(
            college=self.college,
            department=self.compsci,
            course_id='187',
            course_name='Data Structures'
        )

    # test college departments
    def test_college_departments(self):
        num_dep = self.college.departments.all().count()
        self.assertEqual(num_dep, 2)

    # test duplicate key: department
    def test_unique_dep_class(self):
        with self.assertRaises(IntegrityError):
            Department.objects.create(name='Computer Science')

    # test duplicate key: class and subject
    def test_unique_subject_class(self):
        with self.assertRaises(ValidationError):
            CollegeCourse.objects.create(
                college=self.college,
                department=self.compsci,
                course_id='486',
                course_name='Machine Learning'
            )

    # get classes in subject
    def test_get_classes(self):
        num_courses = CollegeCourse.objects.filter(department__name='Computer Science').count()
        self.assertEqual(num_courses, 2)

    # should be able to add class since its a different course number
    def test_class_with_diff_id(self):
        # same as in setUp but differs by class_id
        CollegeCourse.objects.create(
            college=self.college,
            department=self.compsci,
            course_id='586',
            course_name='Machine Learning'
        )
        # get all computer science courses including added one from above
        num_courses = self.college.collegecourse_set.filter(
            department__name='Computer Science'
        ).count()
        self.assertEqual(num_courses, 3)

    # get Computer Science classes in college
    def test_get_classes_in_subject(self):
        num_courses = self.college.collegecourse_set.filter(
            department__name='Computer Science'
        ).count()
        self.assertEqual(num_courses, 2)

    # test getting all college classes
    def test_get_all_college_courses(self):
        CollegeCourse.objects.create(
            college=self.college,
            department=self.history,
            course_id='586',
            course_name='Roman'
        )

        num_courses = self.college.collegecourse_set.all().count()
        self.assertEqual(num_courses, 3)

    # test deletion department. Nothing should happen
    def test_delete_department(self):
        with self.assertRaises(IntegrityError):
            Department.objects.get(name='Computer Science').delete()

    # test deletion college
    def test_delete_college(self):
        College.approved_colleges.get(email_domain='test.edu').delete()
        num_courses = CollegeCourse.objects.all().count()
        num_courses = CollegeCourse.objects.all().count()
        self.assertEqual(num_courses, 0)
