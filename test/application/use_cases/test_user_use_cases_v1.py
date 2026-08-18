from unittest import TestCase
from unittest.mock import MagicMock

from src.adapters.output.credential_provider_adapter_v1 import CredentialProviderAdapterV1
from src.adapters.output.user_repository_adapter_v1 import UserRepositoryAdapterV1
from src.application.exceptions.conflict_exception import ConflictException
from src.application.use_cases.user_use_cases_v1 import UserUseCasesV1
from src.domain.dtos.create_user import CreateUser
from src.domain.dtos.credential_secret import CredentialSecret


class TestUserUseCasesV1(TestCase):
    def setUp(self):
        user_repository = UserRepositoryAdapterV1("todo-list-users")
        credential_provider = CredentialProviderAdapterV1("arn:aws:secretsmanager:us-east-1:123456789012:secret:credentials")
        self.use_cases = UserUseCasesV1(user_repository, credential_provider)

    def test_register_success(self):
        self.use_cases.user_repository.email_exists = MagicMock(return_value=False)
        self.use_cases.user_repository.create = MagicMock(return_value=200)
        credentials = CredentialSecret(
            "dohyie8vaighohc7Ahmahraej7eeshieT5MaiwaxuunoHohv5baiSive2eaSho4r",
            "Liew3aiPia2ba0Ec6oozai2uyeifeer5aiceichoN7ohjae5aiWooX5lemeovai8",
        )
        self.use_cases.credential_provider.get_secret = MagicMock(return_value=credentials)
        dto = CreateUser(
            name="Clive Rosfield",
            email="clive@rosfield.test",
            password="Sur1eeGhe5Aev1Th"
        )
        result = self.use_cases.register(dto)
        self.assertEqual(result.expires_in, 15 * 60)

    def test_register_email_already_registered(self):
        self.use_cases.user_repository.email_exists = MagicMock(return_value=True)
        try:
            dto = CreateUser(
                name="Joshua Rosfield",
                email="joshua@rosfield.test",
                password="za3ohMicooD0Iem3"
            )
            self.use_cases.register(dto)
        except ConflictException as e:
            self.assertIsInstance(e, ConflictException)
