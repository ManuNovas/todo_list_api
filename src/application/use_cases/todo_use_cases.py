from datetime import datetime
from os import getenv
from uuid import uuid4

from aws_lambda_powertools.logging import Logger
from dotenv import load_dotenv
from jwt import decode, ExpiredSignatureError, InvalidSignatureError, DecodeError

from src.application.ports.input.todo_input_port import TodoInputPort
from src.application.ports.output.todo_output_port import TodoOutputPort
from src.domain.dtos.todo_dtos import CreateDto
from src.domain.dtos.user_dtos import BearerTokenDto, TOKEN_ALGORITHM
from src.domain.entities.todo import Todo


class TodoUseCases(TodoInputPort):
    todo_repository: TodoOutputPort
    logger: Logger

    def __init__(self, todo_repository: TodoOutputPort):
        load_dotenv()
        self.todo_repository = todo_repository
        self.logger = Logger(service="TodoUseCases")

    def _get_token_payload(self, token_dto: BearerTokenDto) -> dict:
        secret = getenv("JWT_SECRET_KEY")
        try:
            return decode(token_dto.token, secret, TOKEN_ALGORITHM)
        except (ExpiredSignatureError, InvalidSignatureError, DecodeError) as e:
            self.logger.error(e)
            raise Exception(401, "Unauthorized")

    def create(self, token_dto: BearerTokenDto, create_dto: CreateDto) -> Todo:
        payload = self._get_token_payload(token_dto)
        sk = str(uuid4())
        created_at = datetime.now().isoformat()
        todo = Todo(
            user_pk=payload["pk"],
            todo_sk=sk,
            title=create_dto.title,
            description=create_dto.description,
            created_at=created_at,
        )
        self.todo_repository.create(todo)
        return todo
