from aws_lambda_powertools import Logger
from boto3 import resource
from boto3.dynamodb.conditions import Attr

from src.adapters.output.dynamodb_output_adapter import DynamoDBOutputAdapter
from src.application.ports.output.user_output_port import UserOutputPort
from src.domain.entities.user import User, USER_SK


class UserOutputAdapter(UserOutputPort, DynamoDBOutputAdapter):
    logger: Logger

    def __init__(self, table_name: str):
        dynamodb = resource("dynamodb")
        self.table = dynamodb.Table(table_name)
        self.logger = Logger(service="UserOutputAdapter")

    def _dict_to_user(self, item: dict) -> User:
        return User(
            pk=item["pk"],
            name=item["name"],
            email=item["email"],
            password=item["password"],
            created_at=item["created_at"],
            updated_at=item["updated_at"],
        )

    def email_exists(self, email: str) -> bool:
        response = self.table.scan(FilterExpression=Attr("email").eq(email))
        return response["Count"] > 0

    def create(self, user: User) -> dict:
        return self._put_item(user.__dict__)
    
    def get_by_email(self, email: str) -> User:
        response = self.table.scan(
            FilterExpression=Attr("email").eq(email),
        )
        if response["Count"] == 0:
            self.logger.error(response)
            raise Exception(404, "Email is not found")
        return self._dict_to_user(response["Items"][0])

    def get_by_pk(self, pk: str) -> User:
        response = self.table.get_item(Key={
            "pk": pk,
            "sk": USER_SK,
        })
        if not "Item" in response:
            self.logger.error(response)
            raise Exception(404, "User is not found")
        return self._dict_to_user(response["Item"])
