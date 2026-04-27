from unittest import TestCase
from unittest.mock import MagicMock

from src.adapters.output.user_output_adapter import UserOutputAdapter


class TestUserOutputAdapter(TestCase):
    adapter: UserOutputAdapter

    def setUp(self):
        self.adapter = UserOutputAdapter("todo_users_dev")

    def test_email_exists_false(self):
        self.adapter.table.scan = MagicMock(return_value={
            "Count": 0
        })
        result = self.adapter.email_exists("clive@rosfield.test")
        self.assertFalse(result)

    def test_email_exists_true(self):
        self.adapter.table.scan = MagicMock(return_value={
            "Count": 1
        })
        result = self.adapter.email_exists("joshua@rosfield.test")
        self.assertTrue(result)
