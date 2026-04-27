from abc import ABC, abstractmethod


class UserOutputPort(ABC):
    @abstractmethod
    def email_exists(self, email: str) -> bool:
        pass
