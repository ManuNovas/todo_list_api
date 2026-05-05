from unittest import TestCase
from unittest.mock import MagicMock

from src.adapters.output.todo_output_adapter import TodoOutputAdapter
from src.domain.entities.todo import Todo, TODO_SK


class TestTodoOutputAdapter(TestCase):
    output_adapter: TodoOutputAdapter

    def setUp(self):
        self.output_adapter = TodoOutputAdapter("todo_users_dev")

    def test_create_success(self):
        self.output_adapter.table.put_item = MagicMock(return_value={
            "ResponseMetadata": {
                "HTTPStatusCode": 200,
            },
        })
        todo = Todo(
            user_pk="f8fae484-c975-4e9c-804c-d76731579583",
            todo_sk="a98b5511-4487-4d43-a961-7eeb2be61bb0",
            title="Learn basic black magic spells",
            description="Learn basic spells like fire, thunder and blizzard",
            created_at="2026-05-05T00:43:27.655654",
        )
        result = self.output_adapter.create(todo)
        self.assertEqual(result["ResponseMetadata"]["HTTPStatusCode"], 200)

    def test_create_error(self):
        self.output_adapter.table.put_item = MagicMock(return_value={
            "ResponseMetadata": {
                "HTTPStatusCode": 400,
            },
        })
        todo = Todo(
            user_pk="1",
            todo_sk="1",
            title="Learn basic black magic spells",
            description="Learn basic spells like fire, thunder and blizzard",
            created_at="2026-05-05T00:43:27.655654",
        )
        try:
            self.output_adapter.create(todo)
        except Exception as e:
            self.assertEqual(e.args[0], 400)
