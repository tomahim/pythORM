from security.auth import UserSession
from utils.utils import enum


class ForbiddenActionException(Exception):
    def __init__(self, msg):
        self.msg = msg


class UserNotLoggedException(Exception):
    def __init__(self, msg):
        self.msg = msg


PermissionType = enum(
    'READ_DISCUSSION',
    'ADD_POST',
    'ADD_IDEA',
    'REMOVE_POST',
    'REMOVE_IDEA'
)


def permissions_check(permission):
    """ Decorator to check user permissions on some actions """

    def decorated(func):

        def wrapper(*args, **kwargs):
            user_session = UserSession()
            if not user_session.current_user:
                raise UserNotLoggedException('User should be connected')
            if permission and permission in UserSession.current_user.permissions:
                return func(*args, **kwargs)
            else:
                raise ForbiddenActionException('User not allowed')

        return wrapper

    return decorated
