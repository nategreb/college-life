from django.test import TestCase
from colleges.models import (
    College,
    ResidentialArea,
)


class TestResidentialArea(TestCase):
    def setUp(self):
        self.college = College.all_colleges.create(
            email_domain='test.edu',
            college_name='University Testing',
            state_province='test',
            country='US',
            is_approved=True
        )
        res_hall = ResidentialArea.objects.create(
            college=self.college,
            res_hall_name='testing area'
        )

    # test that creating residential area with just these fields is valid
    def test_secondary_key_valid(self):
        area = ResidentialArea.objects.create(
            college=self.college,
            res_hall_name='testing diff'
        )
        self.assertIsInstance(area, ResidentialArea)
