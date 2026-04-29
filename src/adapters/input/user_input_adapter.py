from aws_lambda_powertools.utilities.validation import validate, SchemaValidationError
from json import loads, dumps

from src.adapters.input.schemas.user_schemas import REGISTER_BODY
from src.application.ports.input.user_input_port import UserInputPort
from src.domain.dtos.user_dtos import CreateDto


class UserInputAdapter:
    input_port: UserInputPort

    def __init__(self, input_port: UserInputPort):
        self.input_port = input_port

    @staticmethod
    def _generate_response(code: int, body: dict):
        return {
            "statusCode": code,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": dumps(body),
        }

    def register(self, event):
        try:
            body = loads(event["body"])
            validate(body, REGISTER_BODY)
            dto = CreateDto(
                name=body["name"],
                email=body["email"],
                password=body["password"],
            )
            token = self.input_port.register(dto)
            response = self._generate_response(201, token.__dict__)
        except SchemaValidationError as e:
            response = self._generate_response(400, {
                "message": e.validation_message,
            })
        except Exception as e:
            args_len = len(e.args)
            response = self._generate_response(
                e.args[0] if args_len > 0 else 500,
                {"message": e.args[1] if args_len > 1 else "Internal server error"},
            )
        return response

