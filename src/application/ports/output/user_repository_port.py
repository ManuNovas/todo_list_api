from abc import ABC, abstractmethod

from src.domain.entities.user import User


class UserRepositoryPort(ABC):
    @abstractmethod
    def email_exists(self, email: str) -> bool:
        pass

    @abstractmethod
    def create(self, user: User) -> int:
        pass
