from abc import ABC, abstractmethod

from src.application.ports.output.credential_provider_port import CredentialProviderPort
from src.application.ports.output.user_repository_port import UserRepositoryPort
from src.domain.dtos.create_user import CreateUser
from src.domain.dtos.token import Token


class UserInputPort(ABC):
    @abstractmethod
    def register(self, dto: CreateUser) -> Token:
        pass
        
