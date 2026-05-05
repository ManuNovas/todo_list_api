from aws_lambda_powertools.logging import Logger
from boto3 import resource

from src.adapters.output.dynamodb_output_adapter import DynamoDBOutputAdapter
from src.application.ports.output.todo_output_port import TodoOutputPort
from src.domain.dtos.todo_dtos import CreateDto
from src.domain.entities.todo import Todo


class TodoOutputAdapter(TodoOutputPort, DynamoDBOutputAdapter):
    logger: Logger

    def __init__(self, table_name: str):
        dynamodb = resource("dynamodb")
        self.table = dynamodb.Table(table_name)
        self.logger = Logger(service="TodoOutputAdapter")

    def create(self, todo: Todo) -> dict:
        return self._put_item(todo.__dict__)
