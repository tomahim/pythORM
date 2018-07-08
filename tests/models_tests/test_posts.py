import unittest

from mock import mock

from models.post import Post
from models.user import User
from security.permission import PermissionType, ForbiddenActionException

mock_user_forbidden = User(
    username='anna',
    email='anna@company.com',
    password='789845'
)
mock_user_forbidden.set_global_permissions([
    'WRONG_PERMISSION'
])

mock_user_allowed_for_create = User(
    username='bob',
    email='bob@company.com',
    password='7857657'
)
mock_user_allowed_for_create.set_global_permissions([
    PermissionType.ADD_POST
])

mock_user_allowed_for_remove = User(
    username='bob',
    email='bob@company.com',
    password='7857657'
)
mock_user_allowed_for_remove.set_global_permissions([
    PermissionType.REMOVE_POST
])


class TestPost(unittest.TestCase):

    @mock.patch("security.auth.UserSession.current_user", mock_user_forbidden)
    def test_post_persist_should_check_create_permission(self):
        with self.assertRaises(ForbiddenActionException) as context:
            post = Post(
                discussion_id='156546',
                text='This is a test post',
                creator_id='453544564'
            ).persist()
        self.assertIsInstance(context.exception, ForbiddenActionException)

    @mock.patch("security.auth.UserSession.current_user", mock_user_forbidden)
    def test_post_reply_with_post_should_check_create_permission(self):
        with self.assertRaises(ForbiddenActionException) as context:
            post = Post(
                discussion_id='156546',
                text='This is a test post',
                creator_id='453544564'
            ).persist()
            post.reply_with_post(Post(
                discussion_id='156546',
                text='This is a test reply',
                creator_id='4535445'
            ))
        self.assertIsInstance(context.exception, ForbiddenActionException)

    @mock.patch("security.auth.UserSession.current_user", mock_user_allowed_for_create)
    def test_post_reply_with_post_should_pass(self):
        post = Post(
            discussion_id='156546',
            text='This is a test post',
            creator_id='453544564'
        ).persist()
        reply = Post(
            discussion_id='156546',
            text='This is a test reply',
            creator_id='4535445'
        )
        post.reply_with_post(reply)
        self.assertEqual(reply.parent_post_id, post.id)
        self.assertEqual(post.posts, [reply])

    @mock.patch("security.auth.UserSession.current_user", mock_user_allowed_for_create)
    def test_post_reply_with_post_should_fail_with_different_discussion_id(self):
        with self.assertRaises(ForbiddenActionException) as context:
            post = Post(
                discussion_id='156546',
                text='This is a test post',
                creator_id='453544564'
            ).persist()
            post.reply_with_post(Post(
                discussion_id='aaaaa',
                text='This is a test reply',
                creator_id='4535445'
            ))

        self.assertIsInstance(context.exception, ForbiddenActionException)

    @mock.patch("security.auth.UserSession.current_user", mock_user_allowed_for_create)
    def test_post_persist_should_pass(self):
        try:
            Post(
                discussion_id='54354654',
                text='This is a test post',
                creator_id='453544564'
            ).persist()

        except ForbiddenActionException:
            self.fail("persist() raised ForbiddenActionException unexpectedly")

    @mock.patch("security.auth.UserSession.current_user", mock_user_forbidden)
    def test_post_delete_should_check_create_permission(self):
        with self.assertRaises(ForbiddenActionException) as context:
            Post(
                discussion_id='156546',
                text='This is a test post',
                creator_id='453544564'
            ).delete()
        self.assertIsInstance(context.exception, ForbiddenActionException)

    @mock.patch("security.auth.UserSession.current_user", mock_user_allowed_for_remove)
    def test_post_delete_should_pass(self):
        try:
            Post(
                discussion_id='54354654',
                text='This is a test post',
                creator_id='453544564'
            ).delete()
        except ForbiddenActionException:
            self.fail("delete() raised ForbiddenActionException unexpectedly")

    def test_post_init_should_set_default_upvote_count(self):
        # when
        post = Post(
            discussion_id='156546',
            text='This is a test post',
            creator_id='453544564'
        )

        # then
        self.assertEqual(post._upvote_count, 0)
