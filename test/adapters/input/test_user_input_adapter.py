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

    def _assert_email_validation(self, result: dict):
        self.assertEqual(result, {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": dumps({
                "message": "data.email must be email",
            }),
        })

    def test_register_success(self):
        bearer_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwayI6IjcxYTQ0NGY1LTRhMjctNDdjOC04ZTM5LWJkOGRlOTllODk5YiJ9.Xlfz_yiFDdrRk9sPlqvsJD2YgeNpjevKunTiPF78ooU"
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
        self._assert_email_validation(result)
    
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

    def test_login_success(self):
        token_dto = TokenDto(
            bearer_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwayI6IjcxYTQ0NGY1LTRhMjctNDdjOC04ZTM5LWJkOGRlOTllODk5YiJ9.Xlfz_yiFDdrRk9sPlqvsJD2YgeNpjevKunTiPF78ooU"
        )
        self.input_adapter.input_port.login = MagicMock(return_value=token_dto)
        result = self.input_adapter.login({
            "body": dumps({
                "email": "clive@rosfield.test",
                "password": "s3cur3p455w0rd"
            }),
        })
        self.assertEqual(result, {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": dumps(token_dto.__dict__),
        })

    def test_login_validation_error(self):
        result = self.input_adapter.login({
            "body": dumps({
                "email": "clive@rosfield",
                "password": "wr0ngp455w0rd",
            }),
        })
        self._assert_email_validation(result)

    def test_login_wrong_credentials(self):
        status_code = 401
        message = "Invalid Credentials"
        self.input_adapter.input_port.login = MagicMock(
            side_effect=Exception(status_code, message),
        )
        result = self.input_adapter.login({
            "body": dumps({
                "email": "clive@rosfield.test",
                "password": "wr0ngp455w0rd",
            }),
        })
        self.assertEqual(result, {
            "statusCode": status_code,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": dumps({
                "message": message,
            }),
        })
