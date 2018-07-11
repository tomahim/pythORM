from datetime import datetime

from core.base import Base, Column, ColumnType
from models.idea import Idea
from models.post import Post


class Discussion(Base):
    """This describes the model for a Discussion.
       Discussion contains Ideas and Posts.
    """

    columns = [
        Column('id', ColumnType.STRING, primary_key=True),
        Column('title', ColumnType.STRING),
        Column('name', ColumnType.STRING),
        Column('description', ColumnType.STRING),
        Column('creator_id', ColumnType.STRING),
        Column('creation_date', ColumnType.DATETIME)
    ]

    def __init__(self, name, title, creator_id, description=None, creation_date=datetime.now(), **kwargs):
        super(Discussion, self).__init__(**kwargs)
        self._id = None
        self._name = name
        self._title = title
        self._description = description
        self._creator_id = creator_id
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
    def creator_id(self):
        return self._creator_id

    @creator_id.setter
    def creator_id(self, creator_id):
        self._creator_id = creator_id

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

    def number_of_posts(self):
        """ Return the total number of posts of the Discussion """
        return len(self.db.find_list_by(Post, 'discussion_id', self.id))

    def number_of_ideas(self):
        """ Return the total number of posts of the Discussion """
        return len(self.db.find_list_by(Idea, 'discussion_id', self.id))

    def all_posts_associated_to_idea(self):
        raise NotImplementedError()

    def all_posts_not_associated_to_idea(self):
        raise NotImplementedError()

    def number_of_participants(self):
        raise NotImplementedError()
