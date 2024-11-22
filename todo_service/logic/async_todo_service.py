from abc import ABC, abstractmethod
from typing import List, Optional

from todo_service.boundaries.todo_boundary import TodoBoundary


class AsyncTodoService(ABC):

    @abstractmethod
    async def get_all_todos(self) -> List[TodoBoundary]:
        ...

    @abstractmethod
    async def get_todo_by_id(self, attr_value: str) -> TodoBoundary:
        ...

    @abstractmethod
    async def get_todo_by_title(self, attr_value: str) -> List[TodoBoundary]:
        ...

    @abstractmethod
    async def get_todo_by_priority(self, attr_value: str) -> List[TodoBoundary]:
        ...

    @abstractmethod
    async def create_todo(self, todo_boundary: TodoBoundary) -> TodoBoundary:
        ...

    @abstractmethod
    async def update_todo(self, todo_id: str, todo_boundary: TodoBoundary) -> Optional[TodoBoundary]:
        ...

    @abstractmethod
    async def delete(self, todo_id: str) -> bool:
        ...
