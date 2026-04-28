from unittest import TestCase
from unittest.mock import MagicMock

from src.adapters.output.user_output_adapter import UserOutputAdapter
from src.application.use_cases.user_use_cases import UserUseCases
from src.domain.dtos.user_dtos import CreateDto


class TestUserUseCases(TestCase):
    use_cases: UserUseCases

    def setUp(self):
        output_adapter = UserOutputAdapter("todo_users_dev")
        self.use_cases = UserUseCases(output_adapter)

    def test_register_success(self):
        self.use_cases.output_port.email_exists = MagicMock(return_value=False)
        self.use_cases.output_port.create = MagicMock(return_value={})
        result = self.use_cases.register(CreateDto(
            name="Clive Rosfield",
            email="clive@rosfield.test",
            password="s3cur3p455w0rd",
        ))
        self.assertIsNotNone(result.bearer_token)
