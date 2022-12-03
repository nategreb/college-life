from django.test import TestCase
from users.models import User
from colleges.models import (
    College,
    ResidentialArea,
    Dorms,
)


class TestDorms(TestCase):
    def setUp(self):
        self.college = College.all_colleges.create(
            email_domain='test.edu',
            college_name='University Testing',
            state_province='test',
            country='US',
            is_approved=True
        )

        self.res_hall = ResidentialArea.objects.create(
            college=self.college,
            res_hall_name='testing area'
        )

        self.admin = User.objects.create_admin(
            'nategreb',
            'ngrebelsky@test.edu',
            'test123'
        )
        # create a mix of dorms with/out Res Area
        for i in range(5):
            res_hall = self.res_hall
            if i > 2:
                res_hall = None
            dorm = Dorms.objects.create(
                dorm_name='test' + str(i),
                college=self.college,
                residentialArea=res_hall
            )

    """
        Test that there are 2 dorms created in setup without res area
    """

    def test_no_res_hall(self):
        self.assertEqual(len(Dorms.objects.filter(college=self.college, residentialArea=None)), 2)

    """
       Test that the above setup only created 3 dorms within the
       res__hall called 'testing area'
    """

    def test_with_res_hall(self):
        self.assertEqual(len(self.res_hall.dorms_set.all()), 3)

    """
        Test that the college created above has 5 dorms total
    """

    def test_college_dorms(self):
        self.assertEqual(len(self.college.dorms_set.all()), 5)
