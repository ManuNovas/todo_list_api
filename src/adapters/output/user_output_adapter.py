from aws_lambda_powertools import Logger
from boto3 import resource
from boto3.dynamodb.conditions import Attr

from src.application.ports.output.user_output_port import UserOutputPort
from src.domain.entities.user import User


class UserOutputAdapter(UserOutputPort):
    logger: Logger

    def __init__(self, table_name: str):
        dynamodb = resource("dynamodb")
        self.table = dynamodb.Table(table_name)
        self.logger = Logger(service="UserOutputAdapter")

    def email_exists(self, email: str) -> bool:
        response = self.table.scan(FilterExpression=Attr("email").eq(email))
        return response["Count"] > 0

    def create(self, user: User) -> dict:
        response = self.table.put_item(Item=user.__dict__)
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            self.logger.error(response)
            raise Exception(response["ResponseMetadata"]["HTTPStatusCode"], "An error ocurred while storing user")
        return response
