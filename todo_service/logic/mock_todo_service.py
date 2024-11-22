import asyncio
from typing import List, Optional

from python_multipart.multipart import Field

from todo_service.boundaries.todo_boundary import TodoBoundary
from todo_service.entities.mock_todo_entity import MockTodoEntity
from todo_service.enums.todo_priority import Priority
from todo_service.logic.async_todo_service import AsyncTodoService


class MockTodoService(AsyncTodoService):
    """
    Mock implementation of an asynchronous TodoTask management service.

    This service provides mock functionality for managing task items, including CRUD operations.
    It uses a simulated response delay (`MOCK_RESPONSE_DELAY`) to mimic real-world network latency.

    Attributes:
        MOCK_RESPONSE_DELAY (float): Simulated delay (in seconds) for asynchronous responses.
        todo_dao (List[TodoBoundary]): A mock database of task entities.
    """

    MOCK_RESPONSE_DELAY = 0.01

    def __init__(self):
        """
        Initializes a new instance of MockTodoService.
        """
        self.todo_dao = None

    def set_todo_dao(self, todo_dao: List[TodoBoundary]):
        """
        Sets the mock task DAO (data access object).

        Args:
            todo_dao (List[TodoBoundary]): List of TaskBoundary objects simulating the database.
        """
        self.todo_dao = todo_dao

    async def get_all_todos(self) -> List[TodoBoundary]:
        """
        Retrieves all task items.

        Returns:
            List[TodoBoundary]: List of all task items.
        """
        await asyncio.sleep(self.MOCK_RESPONSE_DELAY)
        return [TodoBoundary.from_entity(todo_entity) for todo_entity in self.todo_dao]

    async def get_todo_by_id(self, attr_value: str) -> Optional[TodoBoundary]:
        """
        Retrieves a task item by its ID.

        Args:
            attr_value (str): The ID of the task item to retrieve.

        Returns:
            Optional[TodoBoundary]: The task item with the matching ID, or None if not found.
        """
        await asyncio.sleep(self.MOCK_RESPONSE_DELAY)
        return next(
            (TodoBoundary.from_entity(todo_entity) for todo_entity in self.todo_dao if todo_entity.id == attr_value),
            None
        )

    async def get_todo_by_title(self, attr_value: str) -> List[TodoBoundary]:
        """
        Retrieves task items by their title.

        Args:
            attr_value (str): The title to search for.

        Returns:
            List[TodoBoundary]: List of task items with the matching title.
        """
        await asyncio.sleep(self.MOCK_RESPONSE_DELAY)
        return [TodoBoundary.from_entity(todo_entity) for todo_entity in self.todo_dao if
                todo_entity.title == attr_value]

    async def get_todo_by_priority(self, attr_value: str) -> List[TodoBoundary]:
        """
        Retrieves task items by their priority.

        Args:
            attr_value (str): The priority level ("low", "medium", "high").

        Returns:
            List[TodoBoundary]: List of task items with the matching priority.

        Raises:
            ValueError: If the priority is not one of "low", "medium", or "high".
        """
        await asyncio.sleep(self.MOCK_RESPONSE_DELAY)
        try:
            priority = Priority(attr_value.upper())
        except ValueError:
            raise ValueError('Priority can only be "low", "medium" and "high"')
        return [TodoBoundary.from_entity(todo_entity) for todo_entity in self.todo_dao if
                todo_entity.priority == priority]

    async def create_todo(self, todo_boundary: TodoBoundary) -> TodoBoundary:
        """
        Creates a new task item.

        Args:
            todo_boundary (TodoBoundary): The details of the task item to create.

        Returns:
            TodoBoundary: The created task item.
        """
        await asyncio.sleep(self.MOCK_RESPONSE_DELAY)
        todo_entity = MockTodoEntity.from_boundary(todo_boundary)
        self.todo_dao.append(todo_entity)
        return TodoBoundary.from_entity(todo_entity)

    async def update_todo(self, todo_id: str, todo_boundary: TodoBoundary) -> Optional[TodoBoundary]:
        """
        Updates an existing task item.

        Args:
            todo_id (str): The ID of the task item to update.
            todo_boundary (TodoBoundary): Updated details for the task item.

        Returns:
            Optional[TodoBoundary]: The updated task item, or None if not found.
        """
        await asyncio.sleep(self.MOCK_RESPONSE_DELAY)
        todo_entity = next(filter(lambda todo: todo.id == todo_id, self.todo_dao), None)
        if not todo_entity:
            return None
        todo_entity.update(todo_boundary.model_dump())
        return TodoBoundary.from_entity(todo_entity)

    async def delete(self, todo_id: str) -> bool:
        """
        Deletes a task item by its ID.

        Args:
            todo_id (str): The ID of the task item to delete.

        Returns:
            bool: True if the item was successfully deleted, False if not found.
        """
        await asyncio.sleep(self.MOCK_RESPONSE_DELAY)
        todo_entity = next(filter(lambda todo: todo.id == todo_id, self.todo_dao), None)
        if not todo_entity:
            return False
        self.todo_dao.remove(todo_entity)
        return True
