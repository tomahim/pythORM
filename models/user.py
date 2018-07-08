from core.base import Base
from core.column import Column, ColumnType


class User(Base):
    """This describes the model for a User. """

    columns = [
        Column('id', ColumnType.STRING, primary_key=True),
        Column('username', ColumnType.STRING),
        Column('email', ColumnType.STRING),
        Column('password', ColumnType.STRING)
    ]

    def __init__(self, username, email, password, **kwargs):
        super(User, self).__init__(**kwargs)
        self._id = None
        self._username = username
        self._email = email
        self._password = password
        self._permissions = []

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def permissions(self):
        return self._permissions

    @permissions.setter
    def permissions(self, permissions):
        self._permissions = permissions

    def set_global_permissions(self, permissions):
        self.permissions = permissions

