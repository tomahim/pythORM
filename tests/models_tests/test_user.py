import unittest

from models.user import User


class TestUser(unittest.TestCase):

    def test_user_init_should_set_attributes(self):
        user = User(
            username='anna',
            email='anna@company.com',
            password='789845'
        )
        self.assertEqual(user.username, 'anna')
        self.assertEqual(user.email, 'anna@company.com')
        self.assertEqual(user.password, '789845')

    def test_user_set_global_permissions_should_set_permissions(self):
        # given
        user = User(
            username='anna',
            email='anna@company.com',
            password='789845'
        )

        # when
        user.set_global_permissions(['perm1', 'perm2'])

        # then
        self.assertEqual(user.permissions, ['perm1', 'perm2'])
