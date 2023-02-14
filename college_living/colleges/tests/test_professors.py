from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from colleges.models import (
    College,
    Department,
    CollegeCourse,
    Professor
)


class TestProfessors(TestCase):
    def setUp(self):
        self.college = College.all_colleges.create(
            email_domain='test.edu',
            college_name='University Testing',
            state_province='test',
            country='US',
            is_approved=True,
        )

        self.college2 = College.all_colleges.create(
            email_domain='test2.edu',
            college_name='test2',
            state_province='test',
            country='US',
            is_approved=True,
        )

        self.compsci = Department.objects.create(name='Computer Science')

        self.class1 = CollegeCourse.objects.create(
            college=self.college,
            department=self.compsci,
            course_id='486',
            course_name='Machine Learning'
        )

        self.class2 = CollegeCourse.objects.create(
            college=self.college,
            department=self.compsci,
            course_id='100',
            course_name='Diffs'
        )

    """
        Test querying different college's professors
    """

    def test_get_diff_college_professors(self):
        # college
        prof1 = Professor.objects.create(
            college=self.college,
            department=self.compsci,
            first_name='test',
            last_name='test'
        )
        # diff college
        prof2 = Professor.objects.create(
            college=self.college2,
            department=self.compsci,
            first_name='test',
            last_name='test'
        )

        num_profs = Professor.objects.filter(college=self.college2).count()
        self.assertEqual(num_profs, 1)

    """
        test that correct associated professors for class are returned
    """

    def test_multiple_classes(self):
        for fname, lname in (('nate', 'greb'), ('ian', 'lewis'), ('alice', 'bob')):
            prof = Professor.objects.create(
                college=self.college,
                department=self.compsci,
                first_name=fname,
                last_name=lname
            )
            prof.courses.add(self.class1)

        # professor for diff class
        diff = Professor.objects.create(
            college=self.college,
            department=self.compsci,
            first_name='test',
            last_name='test'
        )

        diff.courses.add(self.class2)
        num_profs = Professor.courses.through.objects.filter(
            collegecourse_id=self.class1.id
        ).count()

        self.assertEqual(num_profs, 3)

    """
        get professors classes
    """

    def test_get_professors_classes(self):
        prof = Professor.objects.create(
            college=self.college,
            department=self.compsci,
            first_name='test',
            last_name='test'
        )

        prof.courses.add(self.class2)

        num_courses = prof.courses.count()
        self.assertEqual(num_courses, 1)

    """
        test professor with no courses
    """

    def test_no_courses(self):
        prof = Professor.objects.create(
            college=self.college,
            department=self.compsci,
            first_name='test',
            last_name='test'
        )

        self.assertEqual(prof.courses.count(), 0)

    """
        get professors from different departments
    """

    def test_diff_departments(self):
        for fname, lname in (('nate', 'greb'), ('ian', 'lewis'), ('alice', 'bob')):
            prof = Professor.objects.create(
                college=self.college,
                department=self.compsci,
                first_name=fname,
                last_name=lname
            )
            prof.courses.add(self.class1)

        history = Department.objects.create(name='History')

        # new professor in history department. differs from the above compsci courses
        Professor.objects.create(
            college=self.college,
            department=history,
            first_name='test',
            last_name='test'
        )

        num_profs = Professor.objects.filter(college=self.college, department=history).count()
        self.assertEqual(num_profs, 1)

    """
        get all professors that share a course
    """

    def test_multiple_professors(self):
        for fname, lname in (('nate', 'greb'), ('ian', 'lewis'), ('alice', 'bob')):
            prof = Professor.objects.create(
                college=self.college,
                department=self.compsci,
                first_name=fname,
                last_name=lname
            )
            prof.courses.add(self.class1)

        # query many to many table directly
        num_profs = Professor.courses.through.objects.filter(
            collegecourse_id=self.class1.id
        ).count()

        self.assertEqual(num_profs, 3)

    """
        test that department cant be deleted when referenced by professors
    """

    def test_delete_department(self):
        with self.assertRaises(IntegrityError):
            for fname, lname in (('nate', 'greb'), ('ian', 'lewis'), ('alice', 'bob')):
                prof = Professor.objects.create(
                    college=self.college,
                    department=self.compsci,
                    first_name=fname,
                    last_name=lname
                )
                prof.courses.add(self.class1)

            self.compsci.delete()

            num_profs = Professor.objects.count()

            self.assertEqual(num_profs, 3)

    """
        test slugfield for a new professor
    """

    def test_slugfield(self):
        p1 = Professor.objects.create(
            college=self.college,
            department=self.compsci,
            first_name='test',
            last_name='test'
        )
        self.assertEqual(f'{p1.first_name}-{p1.last_name}', p1.slug)

    """
        test invalid professor w/out first name 
    """

    def test_empty_first_name(self):
        with self.assertRaises(ValidationError):
            Professor.objects.create(
                college=self.college,
                department=self.compsci,
                first_name='testNew'
            ).save()

    """
          test invalid professor w/out last name 
    """

    def test_empty_last_name(self):
        with self.assertRaises(ValidationError):
            Professor.objects.create(
                college=self.college,
                department=self.compsci,
                last_name='testNew'
            ).save()
