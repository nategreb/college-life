from django.test import TestCase
from colleges.models import (
    College
)


class TestCaseColleges(TestCase):
    # setup test database
    def setUp(self):
        College.all_colleges.create(
            email_domain='test.edu',
            college_name='University Testing',
            state_province='test',
            country='US',
            is_approved=True
        )

        College.all_colleges.create(
            email_domain='nonapproved.edu',
            college_name='University Not Approved',
            state_province='test',
            country='US'
        )

    # test college exists and query works
    def test_get_existing_college(self):
        email = 'test@test.edu'
        college = College.all_colleges.get_college(email)
        self.assertEqual(college.email_domain, 'test.edu')

    # test that this email domain doesn't exist
    def test_get_non_existing_college(self):
        email = 'test@non-existing.edu'
        college = College.all_colleges.get_college(email)
        self.assertIsNone(college)

        # test that college is created with just the domain portion 'test.edu'

    def test_department_and_domain_get_college(self):
        email = 'test@med.test.edu'
        college = College.all_colleges.get_college(email)
        self.assertEquals(college.email_domain, 'test.edu')

        # test all college manager with non approved college

    def test_get_non_approved_college(self):
        self.assertEqual(College.all_colleges.filter(email_domain='nonapproved.edu').count(), 1)

    # test approved college managere with approved colleg
    def test_get_approved_college(self):
        self.assertEqual(College.approved_colleges.filter(email_domain='test.edu').count(), 1)

    # test approved college managere with non approved college
    def test_get_non_approved_college_with_approved_manager(self):
        with self.assertRaises(College.DoesNotExist):
            College.approved_colleges.get(email_domain='nonapproved.edu')

