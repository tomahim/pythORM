from datetime import datetime

from core.base import Base
from core.column import Column, ColumnType


class Post(Base):
    """This describes the model for a Post. """

    columns = [
        Column('id', ColumnType.STRING, primary_key=True),
        Column('discussion_id', ColumnType.STRING, foreign_key=True),
        Column('parent_post_id', ColumnType.STRING, foreign_key=True),
        Column('text', ColumnType.STRING),
        Column('creation_date', ColumnType.DATETIME),
    ]

    def __init__(self, discussion_id, text, creation_date=datetime.now(), **kwargs):
        super(Post, self).__init__(**kwargs)
        self._id = None
        self._discussion_id = discussion_id
        self._parent_post_id = None
        self._text = text
        self._creation_date = creation_date

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def discussion_id(self):
        return self._discussion_id

    @discussion_id.setter
    def discussion_id(self, discussion_id):
        self._discussion_id = discussion_id

    @property
    def parent_post_id(self):
        return self._parent_post_id

    @parent_post_id.setter
    def parent_post_id(self, parent_post_id):
        self._parent_post_id = parent_post_id

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
