from models.user import User


class UserSession:
    _current_user = None
    _db = None

    def __init__(self):
        pass

    def connect(self):
        self._current_user = User(
            username='john',
            email='john@company.com',
            password='1234'
        )

    def get_current_user(self):
        return self._current_user