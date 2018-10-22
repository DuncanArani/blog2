import unittest
from app.models import Admin

class AdminModelTest(unittest.TestCase):

    def setUp(self):
        self.new_admin = Admin(password = 'dunco')

    def test_password_setter(self):
        self.assertTrue(self.new_admin.pass_secure is not None)

    def test_no_access_password(self):
            with self.assertRaises(AttributeError):
                self.new_admin.password

    def test_password_verification(self):
        self.assertTrue(self.new_admin.verify_password('dunco'))
