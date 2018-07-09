import unittest
from datetime import datetime

from mock import mock

from models.idea import Idea
from models.post import Post
from models.user import User
from security.permission import ForbiddenActionException, PermissionType

# prepare some tests data

mock_user_forbidden = User(
    username='anna',
    email='anna@company.com',
    password='789845'
)
mock_user_forbidden.set_global_permissions([
    'WRONG_PERMISSION'
])

mock_user_allowed_for_persist = User(
    username='bob',
    email='bob@company.com',
    password='7857657'
)
mock_user_allowed_for_persist.set_global_permissions([
    PermissionType.ADD_IDEA
])

mock_user_allowed_for_delete = User(
    username='bob',
    email='bob@company.com',
    password='7857657'
)
mock_user_allowed_for_delete.set_global_permissions([
    PermissionType.REMOVE_IDEA
])

idea1 = Idea(
    discussion_id='1234',
    title='Test1',
    description='Test1',
    creator_id='1234',
    parent_idea_id=None
)
idea1.id = '1'

idea2 = Idea(
    discussion_id='1234',
    title='Test2',
    description='Test2',
    creator_id='1234',
    parent_idea_id='1'
)
idea2.id = '2'

idea3 = Idea(
    discussion_id='1234',
    title='Test3',
    description='Test3',
    creator_id='1234',
    parent_idea_id='2'
)
idea3.id = '3'

idea4 = Idea(
    discussion_id='1234',
    title='Test4',
    description='Test4',
    creator_id='1234',
    parent_idea_id='1'
)
idea4.id = '4'

idea5 = Idea(
    discussion_id='1234',
    title='Test5',
    description='Test5',
    creator_id='1234',
    parent_idea_id=None
)
idea5.id = '5'

post1 = Post(
    discussion_id='1234',
    text='Test1',
    creator_id='1234',
    parent_post_id=None
)
post1.id = '1'
post1.ideas_ids = ['1', '2', '3']

post2 = Post(
    discussion_id='1234',
    text='Test2',
    creator_id='1234',
    parent_post_id='1'
)
post2.id = '2'
post2.ideas_ids = ['1', '2']

post3 = Post(
    discussion_id='1234',
    text='Test3',
    creator_id='789',
    parent_post_id=None
)
post3.ideas_ids = ['2']
post3.id = '3'

mock_ideas = [idea1, idea2, idea3, idea4]
mock_posts = [post1, post2, post3]


class TestIdea(unittest.TestCase):

    def test_idea_init_should_set_attributes(self):
        idea = Idea(
            discussion_id='54354654',
            creator_id='78987987',
            title='Test idea',
            description='Test description'
        )
        self.assertEqual(idea.discussion_id, '54354654')
        self.assertEqual(idea.creator_id, '78987987')
        self.assertEqual(idea.title, 'Test idea')
        self.assertEqual(idea.description, 'Test description')
        self.assertTrue(isinstance(idea.creation_date, datetime))
        self.assertEqual(idea.ideas, [])

    @mock.patch("security.auth.UserSession.current_user", mock_user_forbidden)
    def test_idea_persist_should_check_create_permission(self):
        with self.assertRaises(ForbiddenActionException) as context:
            idea = Idea(
                discussion_id='54354654',
                creator_id='78987987',
                title='Test idea',
                description='Test description'
            ).persist()
        self.assertIsInstance(context.exception, ForbiddenActionException)

    @mock.patch("security.auth.UserSession.current_user", mock_user_allowed_for_persist)
    def test_idea_persist_should_pass(self):
        try:
            Idea(
                discussion_id='54354654',
                creator_id='78987987',
                title='Test idea',
                description='Test description'
            ).persist()
        except ForbiddenActionException:
            self.fail("persist() raised ForbiddenActionException unexpectedly")

    @mock.patch("security.auth.UserSession.current_user", mock_user_forbidden)
    def test_idea_delete_should_check_delete_permission(self):
        with self.assertRaises(ForbiddenActionException) as context:
            idea = Idea(
                discussion_id='54354654',
                creator_id='78987987',
                title='Test idea',
                description='Test description'
            ).delete()
        self.assertIsInstance(context.exception, ForbiddenActionException)

    @mock.patch("security.auth.UserSession.current_user", mock_user_allowed_for_delete)
    def test_idea_persist_should_pass(self):
        try:
            Idea(
                discussion_id='54354654',
                creator_id='78987987',
                title='Test idea',
                description='Test description'
            ).delete()
        except ForbiddenActionException:
            self.fail("delete() raised ForbiddenActionException unexpectedly")

    @mock.patch("core.base.Base.db.store", dict(
        Idea=mock_ideas
    ))
    def test_idea_get_all_children_ideas_should_pass(self):
        children = idea1.get_all_children_ideas()
        self.assertEqual(len(children), 3)

    @mock.patch("core.base.Base.db.store", dict(
        Idea=mock_ideas,
        Post=mock_posts
    ))
    def test_idea_number_of_messages_should_pass(self):
        nb_messages = idea1.number_of_messages()
        # result should be 3 : post1, post2 and post3 are associated to ideas and sub-ideas to
        # post1 is associated to idea1, idea2, idea3 but should be count for one message
        self.assertEqual(nb_messages, 3)

    @mock.patch("core.base.Base.db.store", dict(
        Idea=mock_ideas,
        Post=mock_posts
    ))
    def test_idea_number_of_participants_should_pass(self):
        nb_participants = idea1.number_of_participants()
        # result should be 2, user '1234' wrote 2 posts, user '456' one post
        self.assertEqual(nb_participants, 2)