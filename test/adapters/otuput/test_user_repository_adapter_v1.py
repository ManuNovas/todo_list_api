from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock
from uuid import uuid4

from src.adapters.output.user_repository_adapter_v1 import UserRepositoryAdapterV1
from src.domain.entities.user import User


class TestUserRepositoryAdapterV1(TestCase):
    def setUp(self):
        self.adapter = UserRepositoryAdapterV1("todo_list_users")

    def test_email_exists(self):
        self.adapter.table.query = MagicMock(return_value={
            "Count": 0,
        })
        result = self.adapter.email_exists("clive@rosfield.test")
        self.assertFalse(result)

    def test_create(self):
        http_status_code = 200
        self.adapter.table.put_item = MagicMock(return_value={
            "ResponseMetadata": {
                "HTTPStatusCode": http_status_code,
            }
        })
        user = User(
            sk=str(uuid4()),
            name="Clive Rosfield",
            email="clive@rosfield.test",
            password="JDJiJDEyJDBzcE5LOGtaRDZITjZiazh4ZXBPQ2V6aWJvMUpyWWtWbzMyVUtOZ042TXBneTRnaWovTFcy",
            created_at=datetime.now().isoformat(),
            updated_at=None,
        )
        result = self.adapter.create(user)
        self.assertEqual(result, http_status_code)
