import asyncio
from asyncio import get_event_loop
from typing import Optional, List

from sqlalchemy.orm import Session

from todo_service.boundaries.todo_boundary import TodoBoundary
from todo_service.entities.todo_entity import TodoEntity
from todo_service.logic.async_todo_service import AsyncTodoService


class TodoService(AsyncTodoService):
    """
    A service for managing tasks with asynchronous operations.

    Provides methods to create, read, update, and delete tasks in the database
    using SQLAlchemy.
    """

    def __init__(self):
        super().__init__()
        self.todo_dao: Optional[Session] = None

    def set_todo_dao(self, todo_dao: Session):
        """
        Set the database session for the service.

        Args:
            todo_dao (Session): The SQLAlchemy session for database operations.
        """
        self.todo_dao = todo_dao

    async def get_all_todos(self) -> List[TodoBoundary]:
        """
        Retrieve all tasks from the database.

        Returns:
            List[TodoBoundary]: A list of task boundary objects.
        """
        loop = asyncio.get_event_loop()

        def query_get_all_todos():
            result = self.todo_dao.query(TodoEntity).all()
            return [TodoBoundary.from_entity(todo_entity) for todo_entity in result]

        return await loop.run_in_executor(executor=None, func=query_get_all_todos)

    async def get_todo_by_id(self, attr_value: str) -> Optional[TodoBoundary]:
        """
        Retrieve a task by its unique identifier.

        Args:
            attr_value (str): The ID of the task.

        Returns:
            Optional[TodoBoundary]: The task boundary object, or None if not found.
        """
        loop = get_event_loop()

        def query_get_todo_by_id():
            todo_entity = self.todo_dao.query(TodoEntity).where(TodoEntity.id == attr_value).one_or_none()
            return TodoBoundary.from_entity(todo_entity) if todo_entity else None

        return await loop.run_in_executor(executor=None, func=query_get_todo_by_id)

    async def get_todo_by_title(self, attr_value: str) -> List[TodoBoundary]:
        """
        Retrieve tasks by their title.

        Args:
            attr_value (str): The title of the tasks.

        Returns:
            List[TodoBoundary]: A list of task boundary objects with the given title.
        """
        loop = get_event_loop()

        def query_get_todo_by_title():
            todo_entities = self.todo_dao.query(TodoEntity).where(TodoEntity.title == attr_value).all()
            return [TodoBoundary.from_entity(todo_entity) for todo_entity in todo_entities]

        return await loop.run_in_executor(executor=None, func=query_get_todo_by_title)

    async def get_todo_by_priority(self, attr_value: str) -> List[TodoBoundary]:
        """
        Retrieve tasks by their priority.

        Args:
            attr_value (str): The priority of the tasks.

        Returns:
            List[TodoBoundary]: A list of task boundary objects with the given priority.
        """
        loop = get_event_loop()

        def query_get_todo_by_priority():
            todo_entities = self.todo_dao.query(TodoEntity).where(TodoEntity.priority == attr_value).all()
            return [TodoBoundary.from_entity(todo_entity) for todo_entity in todo_entities]

        return await loop.run_in_executor(executor=None, func=query_get_todo_by_priority)

    async def create_todo(self, todo_boundary: TodoBoundary) -> TodoBoundary:
        """
        Create a new task in the database.

        Args:
            todo_boundary (TodoBoundary): The task details to create.

        Returns:
            TodoBoundary: The created task boundary object.
        """
        loop = get_event_loop()

        def query_create_todo():
            todo_entity = TodoEntity.from_boundary(todo_boundary)
            self.todo_dao.add(todo_entity)
            self.todo_dao.commit()
            self.todo_dao.refresh(todo_entity)
            return TodoBoundary.from_entity(todo_entity)

        return await loop.run_in_executor(executor=None, func=query_create_todo)

    async def update_todo(self, todo_id: str, todo_boundary: TodoBoundary) -> Optional[TodoBoundary]:
        """
        Update an existing task in the database.

        Args:
            todo_id (str): The ID of the task to update.
            todo_boundary (TodoBoundary): The new task details.

        Returns:
            Optional[TodoBoundary]: The updated task boundary object, or None if not found.
        """
        loop = get_event_loop()

        def query_update_todo():
            todo_entity = self.todo_dao.query(TodoEntity).where(TodoEntity.id == todo_id).one_or_none()
            if not todo_entity:
                return

            todo_entity.update(todo_boundary.model_dump())
            self.todo_dao.add(todo_entity)
            self.todo_dao.commit()
            self.todo_dao.refresh(todo_entity)

            return TodoBoundary.from_entity(todo_entity)

        return await loop.run_in_executor(executor=None, func=query_update_todo)

    async def delete(self, todo_id: str) -> bool:
        """
        Delete a task from the database.

        Args:
            todo_id (str): The ID of the task to delete.

        Returns:
            bool: True if the task was deleted, False if not found.
        """
        loop = get_event_loop()

        def query_update_todo():
            todo_entity = self.todo_dao.query(TodoEntity).where(TodoEntity.id == todo_id).one_or_none()
            if not todo_entity:
                return False

            self.todo_dao.delete(todo_entity)
            return True

        return await loop.run_in_executor(executor=None, func=query_update_todo)
