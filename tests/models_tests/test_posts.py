import unittest

from mock import mock

from models.idea import Idea
from models.post import Post
from models.user import User
from security.permission import PermissionType, ForbiddenActionException

# prepare some tests data

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


post1 = Post(
    discussion_id='1234',
    text='Test1',
    creator_id='1234',
    parent_post_id=None
)
post1.id = '1'

post2 = Post(
    discussion_id='1234',
    text='Test2',
    creator_id='1234',
    parent_post_id='1'
)
post2.id = '2'

post3 = Post(
    discussion_id='1234',
    text='Test3',
    creator_id='1234',
    parent_post_id='2'
)
post3.id = '3'

post4 = Post(
    discussion_id='1234',
    text='Test4',
    creator_id='1234',
    parent_post_id='1'
)
post4.id = '4'

post5 = Post(
    discussion_id='1234',
    text='Test5',
    creator_id='1234',
    parent_post_id='1'
)
post5.id = '4'

idea1 = Idea(
    discussion_id='1234',
    title='Test1',
    description='Test1',
    creator_id='1234',
    parent_idea_id=None
)
idea1.id = '1'

mock_posts = [post1, post2, post3, post4, post5]
mock_ideas = [idea1]


class TestPost(unittest.TestCase):

    def setUp(self):
        print('In method ' + self._testMethodName)

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

    @mock.patch("core.base.Base.db.store", dict(
        Post=mock_posts,
        Idea=mock_ideas
    ))
    def test_post_associate_with_ideas_should_pass(self):
        updated_idea = post1.associate_with_idea(idea1)
        self.assertEqual(updated_idea.parent_post_id, '1')
        self.assertEqual(post1.ideas_ids[0], '1')

    @mock.patch("core.base.Base.db.store", dict(
        Post=mock_posts
    ))
    def test_post_get_all_children_posts_should_pass(self):
        children = post1.get_all_children_posts()
        self.assertEqual(len(children), 4)
