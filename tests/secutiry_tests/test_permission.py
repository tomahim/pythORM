import unittest

from mock import mock

from models.user import User
from security.permission import permissions_check, UserNotLoggedException, ForbiddenActionException, PermissionType


@permissions_check('PERMISSION_1')
def func_to_check():
    return True


mock_user_forbidden = User(
    username='anna',
    email='anna@company.com',
    password='789845'
)
mock_user_forbidden.set_global_permissions([
    'WRONG_PERMISSION'
])

mock_user_allowed = User(
    username='bob',
    email='bob@company.com',
    password='7857657'
)
mock_user_allowed.set_global_permissions([
    'PERMISSION_1'
])


class TestPermission(unittest.TestCase):

    def test_permissions_check_should_raise_exception_if_no_user_connected(self):
        """ Attempt to do an action without permissions """
        with self.assertRaises(UserNotLoggedException) as context:
            func_to_check()
        self.assertIsInstance(context.exception, UserNotLoggedException)

    @mock.patch("security.auth.UserSession.current_user", mock_user_forbidden)
    def test_permissions_check_should_raise_exception_if_no_matching_permissions(self):
        """ Attempt to do action with wrong permission """
        with self.assertRaises(ForbiddenActionException) as context:
            func_to_check()
        self.assertIsInstance(context.exception, ForbiddenActionException)

    @mock.patch("security.auth.UserSession.current_user", mock_user_allowed)
    def test_permissions_check_should_succeed(self):
        self.assertTrue(func_to_check())
