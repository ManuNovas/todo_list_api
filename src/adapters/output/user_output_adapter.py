from boto3 import resource
from boto3.dynamodb.conditions import Attr

from src.application.ports.output.user_output_port import UserOutputPort


class UserOutputAdapter(UserOutputPort):
    def __init__(self, table_name: str):
        dynamodb = resource("dynamodb")
        self.table = dynamodb.Table(table_name)

    def email_exists(self, email: str) -> bool:
        response = self.table.scan(FilterExpression=Attr("email").eq(email))
        return response["Count"] > 0
