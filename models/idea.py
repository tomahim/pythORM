from datetime import datetime

from core.base import Base
from core.column import Column, ColumnType


class Idea(Base):
    """This describes the model for an Idea """

    columns = [
        Column('id', ColumnType.STRING, primary_key=True),
        Column('discussion_id', ColumnType.STRING, foreign_key=True),
        Column('parent_idea_id', ColumnType.STRING),
        Column('title', ColumnType.STRING),
        Column('description', ColumnType.STRING),
        Column('creation_date', ColumnType.DATETIME),
    ]

    def __init__(self, discussion_id, title, description, parent_idea_id=None, creation_date=datetime.now(), **kwargs):
        super(Idea, self).__init__(**kwargs)
        self._id = None
        self._discussion_id = discussion_id
        self._title = title
        self._description = description
        self._parent_idea_id = parent_idea_id
        self._creation_date = creation_date
        self._ideas = []
        self._posts = []

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
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def parent_idea_id(self):
        return self._parent_idea_id

    @parent_idea_id.setter
    def parent_idea_id(self, parent_idea_id):
        self._parent_idea_id = parent_idea_id

    @property
    def creation_date(self):
        return self._creation_date

    @creation_date.setter
    def creation_date(self, creation_date):
        self._creation_date = creation_date

    @property
    def ideas(self):
        return self._ideas

    @ideas.setter
    def ideas(self, ideas):
        self._ideas = ideas

    def add_idea(self, idea):
        idea.parent_idea_id = self.id
        self.ideas.append(idea)