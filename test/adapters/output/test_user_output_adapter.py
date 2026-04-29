from unittest import TestCase
from unittest.mock import MagicMock

from src.adapters.output.user_output_adapter import UserOutputAdapter
from src.domain.entities.user import User, USER_SK


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

    def test_create_success(self):
        user = User(
            pk="63aefdef-b9c0-4270-b984-84a1e17550a1",
            name="Clive Rosfield",
            email="clive@rosfiled.test",
            password="$argon2id$v=19$m=65536,t=3,p=4$bZbvZ6FQZIPesqnNb6eIsA$bHF+Hu97nE0HSWPZoC9bh6hS6jJtCKD1fhbxP6FwoMk",
            created_at="2026-04-28 00:00:00",
            updated_at=None
        )
        self.adapter.table.put_item = MagicMock(return_value={
            "ResponseMetadata": {
                "HTTPStatusCode": 200,
            },
        })
        result = self.adapter.create(user)
        self.assertEqual(result["ResponseMetadata"]["HTTPStatusCode"], 200)

    def test_create_error(self):
        user = User(
            pk="63aefdef-b9c0-4270-b984-84a1e17550a1",
            name="Clive Rosfield",
            email="clive@rosfiled.test",
            password="$argon2id$v=19$m=65536,t=3,p=4$bZbvZ6FQZIPesqnNb6eIsA$bHF+Hu97nE0HSWPZoC9bh6hS6jJtCKD1fhbxP6FwoMk",
            created_at="2026-04-28 00:00:00",
            updated_at=None
        )
        self.adapter.table.put_item = MagicMock(return_value={
            "ResponseMetadata": {
                "HTTPStatusCode": 400,
            },
        })
        try:
            self.adapter.create(user)
        except Exception as exception:
            self.assertEqual(exception.args[0], 400)

    def test_get_by_pk_success(self):
        pk = "63aefdef-b9c0-4270-b984-84a1e17550a1"
        self.adapter.table.get_item = MagicMock(return_value={
            "Item": {
                "pk": pk,
                "sk": USER_SK,
                "name": "Clive Rosfield",
                "email": "clive@rosfield.test",
                "password": "$argon2id$v=19$m=65536,t=3,p=4$bZbvZ6FQZIPesqnNb6eIsA$bHF+Hu97nE0HSWPZoC9bh6hS6jJtCKD1fhbxP6FwoMk",
                "created_at": "2026-04-28 00:00:00",
                "updated_at": None,
            },
        })
        result = self.adapter.get_by_pk(pk)
        self.assertEqual(result.pk, pk)

    def test_get_by_pk_not_found(self):
        self.adapter.table.get_item = MagicMock(return_value={
            "ResponseMetadata": {
                "HTTPStatusCode": 404,
            },
        })
        pk = "invalid-pk"
        try:
            self.adapter.get_by_pk(pk)
        except Exception as e:
            self.assertEqual(e.args[0], 404)
