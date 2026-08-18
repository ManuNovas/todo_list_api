from json import dumps
from unittest import TestCase
from unittest.mock import MagicMock

from src.adapters.output.credential_provider_adapter_v1 import CredentialProviderAdapterV1


class TestCredentialProviderAdapterV1(TestCase):
    def setUp(self):
        self.adapter = CredentialProviderAdapterV1("arn:aws:secretsmanager:us-east-1:123456789012:secret:credentials")

    def test_get_secret(self):
        credentials = {
            "bearer_secret": "dohyie8vaighohc7Ahmahraej7eeshieT5MaiwaxuunoHohv5baiSive2eaSho4r",
            "refresh_secret": "Liew3aiPia2ba0Ec6oozai2uyeifeer5aiceichoN7ohjae5aiWooX5lemeovai8",
        }
        self.adapter.client.get_secret_value = MagicMock(return_value={
            "SecretString": dumps(credentials)
        })
        result = self.adapter.get_secret()
        self.assertEqual(result.bearer_secret, credentials["bearer_secret"])
        self.assertEqual(result.refresh_secret, credentials["refresh_secret"])
