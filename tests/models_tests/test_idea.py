import unittest
from datetime import datetime

from mock import mock

from models.idea import Idea
from models.user import User
from security.permission import ForbiddenActionException, PermissionType

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
