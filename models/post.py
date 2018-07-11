from datetime import datetime

from core.base import Base
from core.column import Column, ColumnType

from security.permission import ForbiddenActionException, PermissionType, permissions_check


class Post(Base):
    """This describes the model for a Post. """

    columns = [
        Column('id', ColumnType.STRING, primary_key=True),
        Column('discussion_id', ColumnType.STRING, foreign_key=True),
        Column('parent_post_id', ColumnType.STRING, foreign_key=True),  # adjacency list relationship
        Column('creator_id', ColumnType.STRING, foreign_key=True),
        Column('text', ColumnType.STRING),
        Column('upvote_count', ColumnType.NUMERIC),
        Column('creation_date', ColumnType.DATETIME),
    ]

    def __init__(self, discussion_id, text, creator_id, parent_post_id=None, parent_idea_id=None, upvote_count=0,
                 creation_date=datetime.now(), **kwargs):
        super(Post, self).__init__(**kwargs)
        self._id = None
        self._discussion_id = discussion_id
        self._creator_id = creator_id
        self._parent_post_id = parent_post_id
        self._parent_idea_id = parent_idea_id
        self._text = text
        self._upvote_count = upvote_count
        self._creation_date = creation_date
        # list of posts that replies to the current post
        self._posts = []
        # list of ideas ids associated to the post
        self._ideas_ids = []

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
    def creator_id(self):
        return self._creator_id

    @creator_id.setter
    def creator_id(self, creator_id):
        self._creator_id = creator_id

    @property
    def parent_post_id(self):
        return self._parent_post_id

    @parent_post_id.setter
    def parent_post_id(self, parent_post_id):
        self._parent_post_id = parent_post_id

    @property
    def parent_idea_id(self):
        return self._parent_idea_id

    @parent_idea_id.setter
    def parent_idea_id(self, parent_idea_id):
        self._parent_idea_id = parent_idea_id

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    @property
    def posts(self):
        return self._posts

    @posts.setter
    def posts(self, posts):
        self._posts = posts

    @property
    def ideas_ids(self):
        return self._ideas_ids

    @ideas_ids.setter
    def ideas_ids(self, ideas_ids):
        self._ideas_ids = ideas_ids

    @permissions_check(PermissionType.ADD_POST)
    def persist(self):
        return super(Post, self).persist()

    @permissions_check(PermissionType.REMOVE_POST)
    def delete(self):
        return super(Post, self).delete()

    @permissions_check(PermissionType.ADD_POST)
    def reply_with_post(self, post):
        """ Reply to the current post by another post
        @:return the persisted reply to the post """
        if post.discussion_id == self.discussion_id:
            post.parent_post_id = self.id
            self.posts.append(post)
            return self.db.upsert(post)
        else:
            raise ForbiddenActionException('Reply to this post not allowed')

    def associate_with_idea(self, idea):
        """ Associate one Post with an Idea
        @:return updated Post """
        if self.discussion_id == idea.discussion_id:
            idea.parent_post_id = self.id
            self.ideas_ids.append(idea.id)
            return self.db.upsert(idea)
        else:
            raise ForbiddenActionException('Cannot associate this post with this idea')

    def get_all_children_posts(self):
        """ Given a Post, retrieve all children posts associated
        @:return list of children of a Post"""
        return self.__find_children_posts(self.db.find_all(self), [self.id])

    def __find_children_posts(self, posts, child_ids):
        """ Recursively build a list of find children posts
        @:return list of children of a Post"""
        children = self.db.find_list_by(self, 'parent_post_id', child_ids, in_operator=True)
        if len(children) > 0:
            return children + self.__find_children_posts(posts, [child.id for child in children])
        else:
            return []

    def print_all_posts(self):
        """ Print a tree representing the Post and its sub-posts """
        print(self.text)
        self.__print_posts_recursively(self.db.find_all(self), self.id)

    def __print_posts_recursively(self, posts, parent_id, level=1):
        """ Recursively print children posts hierarchy
        @:return list of children of an Post"""

        children = self.db.find_list_by(self, 'parent_post_id', parent_id)
        if len(children) > 0:
            for child in children:
                print('    ' * level + child.text)
                self.__print_posts_recursively(posts, child.id, level + 1)
            else:
                level -= 1
