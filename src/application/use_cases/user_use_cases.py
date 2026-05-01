from argon2 import PasswordHasher
from datetime import datetime
from dotenv import load_dotenv
from jwt import encode
from os import getenv
from uuid import uuid4

from src.application.ports.input.user_input_port import UserInputPort
from src.application.ports.output.user_output_port import UserOutputPort
from src.domain.dtos.user_dtos import CreateDto, TokenDto, LoginDto
from src.domain.entities.user import User

load_dotenv()

class UserUseCases(UserInputPort):
    output_port: UserOutputPort

    def __init__(self, output_port: UserOutputPort):
        self.output_port = output_port

    def _create_token(self, user: User) -> TokenDto:
        bearer_payload = {
            "pk": user.pk,
        }
        secret = getenv("JWT_SECRET_KEY")
        return TokenDto(
            bearer_token=encode(bearer_payload, secret, "HS256"),
        )

    def register(self, dto: CreateDto) -> TokenDto:
        if self.output_port.email_exists(dto.email):
            raise Exception(400, "Email already registered")
        ph = PasswordHasher()
        user = User(
            pk=str(uuid4()),
            name=dto.name,
            email=dto.email,
            password=ph.hash(dto.password),
            created_at=datetime.now().isoformat(),
            updated_at=None
        )
        self.output_port.create(user)
        return self._create_token(user)
    
    def login(self, dto: LoginDto) -> TokenDto:
        user = self.output_port.get_by_email(dto.email)
        ph = PasswordHasher()
        if not ph.verify(user.password, dto.password):
            raise Exception(401, "Invalid credentials")
        return self._create_token(user)
