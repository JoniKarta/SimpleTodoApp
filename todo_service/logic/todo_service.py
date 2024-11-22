from typing import Optional, List

from todo_service.boundaries.todo_boundary import TodoBoundary
from todo_service.logic.async_todo_service import AsyncTodoService


class TodoService(AsyncTodoService):
    async def get_all_todos(self) -> List[TodoBoundary]:
        pass

    async def get_todo_by_id(self, attr_value: str) -> TodoBoundary:
        pass

    async def get_todo_by_title(self, attr_value: str) -> List[TodoBoundary]:
        pass

    async def get_todo_by_priority(self, attr_value: str) -> List[TodoBoundary]:
        pass

    async def create_todo(self, todo_boundary: TodoBoundary) -> TodoBoundary:
        pass

    async def update_todo(self, todo_id: str, todo_boundary: TodoBoundary) -> Optional[TodoBoundary]:
        pass

    async def delete(self, todo_id: str) -> bool:
        pass
