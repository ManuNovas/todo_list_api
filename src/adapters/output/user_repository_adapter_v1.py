from aws_lambda_powertools import Logger
from boto3 import resource
from boto3.dynamodb.conditions import Key
from src.application.ports.output.user_repository_port import UserRepositoryPort
from src.domain.entities.user import USER_EMAIL_INDEX, USER_PK, User


class UserRepositoryAdapterV1(UserRepositoryPort):
    USER_NOT_STORED = "USER_NOT_STORED"

    def __init__(self, table_name: str):
        dynamodb = resource("dynamodb")
        self.table = dynamodb.Table(table_name)
        self.logger = Logger(service="UserRepositoryAdapterV1")

    def email_exists(self, email: str) -> bool:
        key_condition_expression = Key("pk").eq(USER_PK) & Key("email").eq(email)
        result = self.table.query(IndexName=USER_EMAIL_INDEX, Limit=1, KeyConditionExpression=key_condition_expression)
        self.logger.info("User retrieved from database", extra={"result": result})
        return result["Count"] > 0

    def create(self, user: User) -> int:
        result = self.table.put_item(Item=user.__dict__)
        self.logger.info("User stored in database", extra={"result": result})
        return result["ResponseMetadata"]["HTTPStatusCode"]
