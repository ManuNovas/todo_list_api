from bcrypt import gensalt, hashpw
from datetime import datetime, timedelta
from jwt import encode
from uuid import uuid4

from src.application.exceptions.conflict_exception import ConflictException
from src.application.ports.input.user_input_port import UserInputPort
from src.application.ports.output.credential_provider_port import CredentialProviderPort
from src.application.ports.output.user_repository_port import UserRepositoryPort
from src.domain.dtos.create_user import CreateUser
from src.domain.dtos.token import Token
from src.domain.dtos.token_payload import TokenPayload
from src.domain.entities.user import User


class UserUseCasesV1(UserInputPort):
    ALGORITHM = "HS256"

    def __init__(
        self,
        user_repository: UserRepositoryPort,
        credential_provider: CredentialProviderPort
    ):
        self.user_repository = user_repository
        self.credential_provider = credential_provider

    def _get_token(self, user: User) -> Token:
        bearer_expiration = datetime.now() + timedelta(minutes=15)
        bearer_payload = TokenPayload(sk=user.sk, exp=bearer_expiration)
        credential_secret = self.credential_provider.get_secret()
        bearer_token = encode(
            bearer_payload.__dict__,
            credential_secret.bearer_secret,
            algorithm=self.ALGORITHM,
        )
        refresh_expiration = datetime.now() + timedelta(days=30)
        refresh_payload = TokenPayload(sk=user.sk, exp=refresh_expiration)
        refresh_token = encode(
            refresh_payload.__dict__,
            credential_secret.refresh_secret,
            algorithm=self.ALGORITHM,
        )
        return Token(
            bearer_token=bearer_token,
            expires_in=15 * 60,
            refresh_token=refresh_token,
        )

    def register(self, dto: CreateUser) -> Token:
        if self.user_repository.email_exists(dto.email):
            raise ConflictException("Email already registered")
        sk = str(uuid4())
        encoded_password = dto.password.encode("utf-8")
        salt = gensalt()
        hashed_password = hashpw(encoded_password, salt)
        user = User(
            sk=sk,
            name=dto.name,
            email=dto.email,
            password=hashed_password,
            created_at=datetime.now().isoformat(),
            updated_at=None
        )
        self.user_repository.create(user)
        return self._get_token(user)
