from core.persistence import DbException
from models.idea import Idea
from models.post import Post
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


class ApiController(UserSession):

    def update_idea(self, idea):
        db = self.get_db()
        return db.update(idea)

    def associate_with_idea(self, idea_to_associate, idea_id):
        """ Associate one idea with another by its idea
        @:return updated Idea """
        db = self.get_db()
        idea = db.find_by_id(Idea, idea_id)
        if idea and idea.discussion_id == idea_to_associate.discussion_id:
            idea_to_associate.parent_idea_id = idea_id
            return db.update(idea_to_associate)
        else:
            raise DbException('Parent idea not found')

    def reply_to_post(self, post_reply, post_id):
        """ Associate one idea with another by its idea
        @:return updated Idea """
        db = self.get_db()
        post = db.find_by_id(Post, post_id)
        if post and post.discussion_id == post_reply.discussion_id:
            post_reply.parent_post_id = post_id
            return db.update(post_reply)
        else:
            raise DbException('Parent post not found')

    def get_all_children_posts(self, post_id):
        """ Given a Post id, retrieve all children posts associated
        @:return list of children of a Post"""
        db = self.get_db()
        direct_children_posts = self.get_db().find_list_by(Post, 'parent_post_id', post_id)
        return self.find_children_posts(direct_children_posts, post_id)

    def find_children_posts(self, posts, obj_id):
        """ Recursively find children posts
        @:return list of children of a Post"""
        children_posts = self.get_db().find_list_by(Post, 'parent_post_id', obj_id)
        if len(children_posts) > 0:
            return children_posts + self.find_children_posts(posts, getattr(children_posts[0], 'id'))
        else:
            return children_posts