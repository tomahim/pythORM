from core.base import Base
from core.column import Column, ColumnType
from datetime import datetime


class Discussion(Base):
    """This describes the model for a Discussion.
       Discussion contains Ideas and Posts.
    """

    columns = [
        Column('id', ColumnType.STRING, primary_key=True),
        Column('title', ColumnType.STRING),
        Column('name', ColumnType.STRING),
        Column('description', ColumnType.STRING),
        Column('creation_date', ColumnType.DATETIME)
    ]

    def __init__(self, name, title, description=None, creation_date=datetime.now(), **kwargs):
        super(Discussion, self).__init__(**kwargs)
        self._id = None
        self._name = name
        self._title = title
        self._description = description
        self._creation_date = creation_date
        self._posts = []

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def creation_date(self):
        return self._creation_date

    @creation_date.setter
    def creation_date(self, creation_date):
        self._creation_date = creation_date

    @property
    def posts(self):
        return self._posts

    @posts.setter
    def posts(self, posts):
        self._posts = posts

    def add_post(self, post):
        self._posts = self.posts + post


if __name__ == "__main__":
    discussion1 = Discussion(
        name='Discussion about environmental issues',
        title='How to deal with the environmental issue caused by cars ?',
        creation_date=datetime.now()
    )
    print(discussion1.name)
