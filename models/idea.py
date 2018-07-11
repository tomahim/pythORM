from datetime import datetime

from core.base import Base, Column, ColumnType
from core.persistence import JoinType
from models.post import Post
from security.permission import ForbiddenActionException, PermissionType, permissions_check


class Idea(Base):
    """This describes the model for an Idea """

    columns = [
        Column('id', ColumnType.STRING, primary_key=True),
        Column('discussion_id', ColumnType.STRING, foreign_key=True),
        Column('parent_idea_id', ColumnType.STRING, foreign_key=True),  # Adjacency list relationship
        Column('creator_id', ColumnType.STRING, foreign_key=True),
        Column('title', ColumnType.STRING),
        Column('description', ColumnType.STRING),
        Column('creation_date', ColumnType.DATETIME),
    ]

    def __init__(self, discussion_id, title, description, creator_id, parent_idea_id=None, creation_date=datetime.now(),
                 **kwargs):
        super(Idea, self).__init__(**kwargs)
        self._id = None
        self._discussion_id = discussion_id
        self._creator_id = creator_id
        self._title = title
        self._description = description
        self._parent_idea_id = parent_idea_id
        self._creation_date = creation_date
        self._ideas = []

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
    def ideas(self):
        return self._ideas

    @ideas.setter
    def ideas(self, ideas):
        self._ideas = ideas

    @permissions_check(PermissionType.ADD_IDEA)
    def persist(self):
        return super(Idea, self).persist()

    @permissions_check(PermissionType.REMOVE_IDEA)
    def delete(self):
        return super(Idea, self).delete()

    def associate_to_idea(self, idea):
        """ Define an Idea as a sub-idea for the current Idea
        @:return updated Idea """
        if self.discussion_id == idea.discussion_id:
            idea.parent_idea_id = self.id
            self.ideas.append(idea)
            return self.db.upsert(idea)
        else:
            raise ForbiddenActionException('')

    def get_all_children_ideas(self):
        """ Given an Idea, retrieve all children ideas associated
        @:return list of children of an Idea"""
        return self.__find_children_ideas(self.db.find_all(self), [self.id])

    def __find_children_ideas(self, ideas, children_ids):
        """ Recursively find children ideas
        @:return list of children of an Idea"""
        children = self.db.find_list_by(self, 'parent_idea_id', children_ids, in_operator=True)
        if len(children) > 0:
            return children + self.__find_children_ideas(ideas, [child.id for child in children])
        else:
            return []

    def __get_posts_associated_to_idea(self):
        """ Get all posts associated to an idea including the posts associated to sub-ideas
        @:return list of post """
        # retrieve all children ideas ids including the current idea
        ideas_ids = [self.id] + [idea.id for idea in self.get_all_children_ideas()]
        # get each posts matching at least on of these ids
        return self.db.find_list_by(Post, 'ideas_ids', ideas_ids, in_operator=True, join=JoinType.LEFT)

    def number_of_messages(self):
        """ Retrieve number of Posts associated to the Idea
        @:return number"""
        posts_associated = self.__get_posts_associated_to_idea()
        # exclude redundant ids
        unique_posts = {post_id for post_id in [post.id for post in posts_associated]}
        return len(unique_posts)

    def number_of_participants(self):
        """ Retrieve number of users who posted something about this Idea
        @:return number"""
        # exclude redundant ids
        unique_users = {creator_id for creator_id in
                        [post.creator_id for post in self.__get_posts_associated_to_idea()]}

        return len(unique_users)

    def print_all_ideas(self):
        """ Print a tree representing the Idea and its sub-ideas """
        print(self.title)
        self.__print_ideas_recursively(self.db.find_all(self), self.id)

    def __print_ideas_recursively(self, ideas, parent_id, level=1):
        """ Recursively print children ideas hierarchy
        @:return list of children of an Idea"""

        children = self.db.find_list_by(self, 'parent_idea_id', parent_id)
        if len(children) > 0:
            for child in children:
                print('    ' * level + child.title)
                self.__print_ideas_recursively(ideas, child.id, level + 1)
            else:
                level -= 1
