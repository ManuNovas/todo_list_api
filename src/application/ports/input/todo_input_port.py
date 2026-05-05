from abc import ABC, abstractmethod

from src.domain.dtos.todo_dtos import CreateDto
from src.domain.dtos.user_dtos import BearerTokenDto
from src.domain.entities.todo import Todo


class TodoInputPort(ABC):
    @abstractmethod
    def create(self, token_dto: BearerTokenDto, create_dto: CreateDto) -> Todo:
        pass
