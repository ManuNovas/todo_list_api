from abc import ABC, abstractmethod

from src.domain.entities.user import User


class UserOutputPort(ABC):
    @abstractmethod
    def email_exists(self, email: str) -> bool:
        pass

    @abstractmethod
    def create(self, user: User) -> dict:
        pass

    @abstractmethod
    def get_by_pk(self, pk: str) -> User:
        pass
