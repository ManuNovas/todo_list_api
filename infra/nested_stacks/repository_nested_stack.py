from aws_cdk import NestedStack
from aws_cdk.aws_dynamodb import TableV2, Attribute, AttributeType, GlobalSecondaryIndexPropsV2
from constructs import Construct
from src.domain.entities.user import USER_EMAIL_INDEX


class RepositoryNestedStack(NestedStack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        users_partition_key = Attribute(name="pk", type=AttributeType.STRING)
        users_sort_key = Attribute(name="sk", type=AttributeType.STRING)
        users_email_attribute = Attribute(name="email", type=AttributeType.STRING)
        users_global_secondary_indexes = [
            GlobalSecondaryIndexPropsV2(
                index_name=USER_EMAIL_INDEX,
                partition_key=users_partition_key,
                sort_key=users_email_attribute,
            )
        ]
        self.users_table = TableV2(
            self,
            "UsersTable",
            table_name="todo_list_users",
            partition_key=users_partition_key,
            sort_key=users_sort_key,
            global_secondary_indexes=users_global_secondary_indexes
        )
