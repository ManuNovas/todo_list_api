from unittest import TestCase
from unittest.mock import MagicMock

from src.adapters.output.user_output_adapter import UserOutputAdapter
from src.application.use_cases.user_use_cases import UserUseCases
from src.domain.dtos.user_dtos import CreateDto, LoginDto
from src.domain.entities.user import User


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
    
    def test_register_email_exists(self):
        self.use_cases.output_port.email_exists = MagicMock(return_value=True)
        self.use_cases.output_port.create = MagicMock(return_value={})
        try:
            self.use_cases.register(CreateDto(
                name="Clive Rosfield",
                email="clive@rosfield.test",
                password="s3cur3p455w0rd",
            ))
        except Exception as e:
            self.assertEqual(e.args[0], 400)

    def test_login_success(self):
        self.use_cases.output_port.get_by_email = MagicMock(return_value=User(
            pk="5a1dd332-e765-4cca-87e5-ceac7d019f65",
            name="Clive Rosfield",
            email="clive@rosfield.test",
            password="$argon2id$v=19$m=65536,t=3,p=4$tnxVKw/xsx9wE1OFMoQXjw$4L4vUKSx4yZLEivKzMT5bXDWF09c15OShucJGLh7pVI",
            created_at="2026-04-30 00:00:00",
            updated_at=None,
        ))
        result = self.use_cases.login(LoginDto(
            email="clive@rosfield.test",
            password="33dyA(?bsci1ecQb",
        ))
        self.assertIsNotNone(result.bearer_token)
