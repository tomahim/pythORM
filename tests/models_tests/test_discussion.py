import unittest
from datetime import datetime

from models.discussion import Discussion


class TestDiscussion(unittest.TestCase):

    def test_discussion_init_should_set_a_default_creation_date(self):
        # when
        discussion = Discussion(
            name='Test discussions',
            title='This is a test discussion',
            creator_id='453544564'
        )

        # then
        self.assertTrue(isinstance(discussion.creation_date, datetime))
