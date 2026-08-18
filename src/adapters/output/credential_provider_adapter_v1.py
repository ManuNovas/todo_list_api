from boto3 import client
from aws_lambda_powertools.logging import Logger
from json import loads

from src.application.ports.output.credential_provider_port import CredentialProviderPort
from src.domain.dtos.credential_secret import CredentialSecret


class CredentialProviderAdapterV1(CredentialProviderPort):
    def __init__(self, secret_arn: str):
        self.secret_arn = secret_arn
        self.client = client("secretsmanager")
        self.logger = Logger(service="CredentialProviderAdapterV1")

    def get_secret(self) -> CredentialSecret:
        result = self.client.get_secret_value(SecretId=self.secret_arn)
        credential = loads(result["SecretString"])
        return CredentialSecret(credential["bearer_secret"], credential["refresh_secret"])
