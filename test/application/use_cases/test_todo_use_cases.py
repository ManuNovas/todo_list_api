from unittest import TestCase
from unittest.mock import MagicMock

from src.adapters.output.todo_output_adapter import TodoOutputAdapter
from src.application.use_cases.todo_use_cases import TodoUseCases
from src.domain.dtos.todo_dtos import CreateDto
from src.domain.dtos.user_dtos import BearerTokenDto


class TestTodoUseCases(TestCase):
    use_cases: TodoUseCases

    def setUp(self):
        todo_repository = TodoOutputAdapter("todo_users_dev")
        self.use_cases = TodoUseCases(todo_repository)

    def test_create_success(self):
        self.use_cases.todo_repository.create = MagicMock(return_value={
            "ResponseMetadata": {
                "HTTPStatusCode": 200,
            },
        })
        token_dto = BearerTokenDto(
            token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwayI6IjcxYTQ0NGY1LTRhMjctNDdjOC04ZTM5LWJkOGRlOTllODk5YiJ9.Xlfz_yiFDdrRk9sPlqvsJD2YgeNpjevKunTiPF78ooU",
        )
        create_dto = CreateDto(
            title="Learn basic black magic spells",
            description="Learn spells like fire, thunder and blizzard",
        )
        result = self.use_cases.create(token_dto, create_dto)
        self.assertEqual(result.title, create_dto.title)
        self.assertEqual(result.description, create_dto.description)

    def test_create_unauthorized(self):
        token_dto = BearerTokenDto(
            token="f4k3t0k3n",
        )
        create_dto = CreateDto(
            title="Learn basic black magic spells",
            description="Learn spells like fire, thunder and blizzard",
        )
        try:
            self.use_cases.create(token_dto, create_dto)
        except Exception as e:
            self.assertEqual(e.args[0], 401)
