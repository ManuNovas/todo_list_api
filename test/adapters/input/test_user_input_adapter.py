from json import dumps
from unittest import TestCase
from unittest.mock import MagicMock

from src.adapters.input.user_input_adapter import UserInputAdapter
from src.adapters.output.user_output_adapter import UserOutputAdapter
from src.application.use_cases.user_use_cases import UserUseCases
from src.domain.dtos.user_dtos import TokenDto


class TestUserInputAdapter(TestCase):
    input_adapter: UserInputAdapter

    def setUp(self):
        output_adapter = UserOutputAdapter("todo_users_dev")
        use_cases = UserUseCases(output_adapter)
        self.input_adapter = UserInputAdapter(use_cases)

    def test_register_success(self):
        bearer_token = "ZlR0UxGgd7WbqiSP894p19UKgBvYWwpqp9F805GoexC9ACe40hbTl5MeQX14R5WU"
        self.input_adapter.input_port.register = MagicMock(return_value=TokenDto(
            bearer_token=bearer_token,
        ))
        result = self.input_adapter.register({
            "body": dumps({
                "name": "Clive Rosfield",
                "email": "clive@rosfield.test",
                "password": "s3cur3p455w0rd",
            })
        })
        self.assertEqual(result, {
            "statusCode": 201,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": dumps({
                "bearer_token": bearer_token,
            }),
        })
    
    def test_register_validation_error(self):
        result = self.input_adapter.register({
            "body": dumps({
                "name": "Clive Rosfield",
                "email": "clive@rosfield",
                "password": "s3cur3p455w0rd",
            })
        })
        self.assertEqual(result, {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": dumps({
                "message": "data.email must be email",
            }),
        })
    
    def test_register_email_registered(self):
        self.input_adapter.input_port.register = MagicMock(side_effect=Exception(400, "Email already registered"))
        result = self.input_adapter.register({
            "body": dumps({
                "name": "Clive Rosfield",
                "email": "clive@rosfield.test",
                "password": "s3cur3p455w0rd",
            })
        })
        self.assertEqual(result, {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": dumps({
                "message": "Email already registered",
            }),
        })
