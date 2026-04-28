from abc import ABC, abstractmethod

from src.domain.dtos.user_dtos import CreateDto, TokenDto


class UserInputPort(ABC):
    @abstractmethod
    def register(self, dto: CreateDto) -> TokenDto:
        pass
