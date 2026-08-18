from aws_cdk import NestedStack
from aws_cdk.aws_secretsmanager import Secret
from constructs import Construct


class ProviderNestedStack(NestedStack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        credential_secret_name = "todo_list_credentials"
        self.credential_secret = Secret(
            self,
            "CredentialSecret",
            secret_name=credential_secret_name
        )
