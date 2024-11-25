from abc import ABC, abstractmethod
from typing import List, Optional

from todo_service.boundaries.todo_boundary import TodoBoundary
from todo_service.dal.pagination import Pagination


class AsyncTodoService(ABC):

    @abstractmethod
    async def get_all_todos(self, pagination_query: Pagination) -> List[TodoBoundary]:
        ...

    @abstractmethod
    async def get_todo_by_id(self, attr_value: str, *args) -> Optional[TodoBoundary]:
        ...

    @abstractmethod
    async def get_todo_by_title(self, attr_value: str, pagination_query: Pagination) -> List[TodoBoundary]:
        ...

    @abstractmethod
    async def get_todo_by_priority(self, attr_value: str, pagination_query: Pagination) -> List[TodoBoundary]:
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
