from abc import ABC, abstractmethod

from src.domain.dtos.credential_secret import CredentialSecret


class CredentialProviderPort(ABC):
    def get_secret(self) -> CredentialSecret:
        pass
