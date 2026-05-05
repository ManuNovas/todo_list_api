from abc import ABC, abstractmethod

from src.domain.entities.todo import Todo


class TodoOutputPort(ABC):
    @abstractmethod
    def create(self, todo: Todo) -> dict:
        pass