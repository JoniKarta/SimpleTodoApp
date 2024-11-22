from asyncio import get_event_loop
from typing import Optional, List

from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from todo_service.boundaries.todo_boundary import TodoBoundary
from todo_service.dal.pagination import Pagination
from todo_service.entities.todo_entity import TodoEntity
from todo_service.logic.async_todo_service import AsyncTodoService


class TodoService(AsyncTodoService):
    """
    A service for managing tasks with asynchronous operations.

    Provides methods to create, read, update, and delete tasks in the database
    using SQLAlchemy. Each method interacts with the database asynchronously,
    leveraging SQLAlchemy ORM and asyncio for non-blocking I/O operations.
    """

    def __init__(self):
        super().__init__()
        self._todo_dao: Optional[Session] = None

    def set_todo_dao(self, todo_dao: Session) -> None:
        """
        Set the database session for the service.

        This method allows setting the SQLAlchemy session that will be used for
        database operations. It must be called before any database interactions.

        Args:
            todo_dao (Session): The SQLAlchemy session for database operations.
        """
        self._todo_dao = todo_dao

    async def get_all_todos(self, pagination_query: Pagination) -> List[TodoBoundary]:
        """
        Retrieve all tasks from the database with pagination support.

        This method queries the database to retrieve all tasks, applying pagination
        parameters such as offset, limit, and sorting.

        Args:
            pagination_query (Pagination): Pagination and sorting parameters.

        Returns:
            List[TodoBoundary]: A list of task boundary objects.
        """
        loop = get_event_loop()

        def query_get_all_todos():
            offset, limit, order_by = pagination_query.offset(), pagination_query.size, pagination_query.order_by
            order_by_with_direction = desc(order_by) if pagination_query.desc else asc(order_by)
            result = (self._todo_dao.query(TodoEntity)
                      .order_by(order_by_with_direction)
                      .offset(offset)
                      .limit(limit)
                      .all())
            return [TodoBoundary.from_entity(todo_entity) for todo_entity in result]

        return await loop.run_in_executor(executor=None, func=query_get_all_todos)

    async def get_todo_by_id(self, attr_value: str, *args) -> Optional[TodoBoundary]:
        """
        Retrieve a task by its unique identifier.

        This method queries the database for a task with the specified ID.

        Args:
            attr_value (str): The ID of the task.

        Returns:
            Optional[TodoBoundary]: The task boundary object if found, or None if not found.
        """
        loop = get_event_loop()

        def query_get_todo_by_id():
            todo_entity = self._todo_dao.query(TodoEntity).where(TodoEntity.id == attr_value).one_or_none()
            return TodoBoundary.from_entity(todo_entity) if todo_entity else None

        return await loop.run_in_executor(executor=None, func=query_get_todo_by_id)

    async def get_todo_by_title(self, attr_value: str, pagination_query: Pagination) -> List[TodoBoundary]:
        """
        Retrieve tasks by their title with pagination support.

        This method queries the database for tasks with a matching title, applying
        pagination parameters such as offset, limit, and sorting.

        Args:
            attr_value (str): The title of the tasks.
            pagination_query (Pagination): Pagination and sorting parameters.

        Returns:
            List[TodoBoundary]: A list of task boundary objects matching the title.
        """
        loop = get_event_loop()

        def query_get_todo_by_title():
            offset, limit, order_by = pagination_query.offset(), pagination_query.size, pagination_query.order_by
            order_by_with_direction = desc(order_by) if pagination_query.desc else asc(order_by)
            todo_entities = (self._todo_dao.query(TodoEntity)
                             .where(TodoEntity.title == attr_value)
                             .order_by(order_by_with_direction)
                             .offset(offset)
                             .limit(limit)
                             .all())
            return [TodoBoundary.from_entity(todo_entity) for todo_entity in todo_entities]

        return await loop.run_in_executor(executor=None, func=query_get_todo_by_title)

    async def get_todo_by_priority(self, attr_value: str, pagination_query: Pagination) -> List[TodoBoundary]:
        """
        Retrieve tasks by their priority with pagination support.

        This method queries the database for tasks with a matching priority, applying
        pagination parameters such as offset, limit, and sorting.

        Args:
            attr_value (str): The priority of the tasks.
            pagination_query (Pagination): Pagination and sorting parameters.

        Returns:
            List[TodoBoundary]: A list of task boundary objects matching the priority.
        """
        loop = get_event_loop()

        def query_get_todo_by_priority():
            offset, limit, order_by = pagination_query.offset(), pagination_query.size, pagination_query.order_by
            order_by_with_direction = desc(order_by) if pagination_query.desc else asc(order_by)
            todo_entities = (self._todo_dao.query(TodoEntity)
                             .where(TodoEntity.priority == attr_value)
                             .order_by(order_by_with_direction)
                             .offset(offset)
                             .limit(limit)
                             .all())
            return [TodoBoundary.from_entity(todo_entity) for todo_entity in todo_entities]

        return await loop.run_in_executor(executor=None, func=query_get_todo_by_priority)

    async def create_todo(self, todo_boundary: TodoBoundary) -> TodoBoundary:
        """
        Create a new task in the database.

        This method accepts a `TodoBoundary` object, converts it into a `TodoEntity`,
        and saves it to the database.

        Args:
            todo_boundary (TodoBoundary): The task details to create.

        Returns:
            TodoBoundary: The created task boundary object.
        """
        loop = get_event_loop()

        def query_create_todo():
            todo_entity = TodoEntity.from_boundary(todo_boundary)
            self._todo_dao.add(todo_entity)
            self._todo_dao.commit()
            self._todo_dao.refresh(todo_entity)
            return TodoBoundary.from_entity(todo_entity)

        return await loop.run_in_executor(executor=None, func=query_create_todo)

    async def update_todo(self, todo_id: str, todo_boundary: TodoBoundary) -> Optional[TodoBoundary]:
        """
        Update an existing task in the database.

        This method searches for a task by its ID, and if found, updates its details
        using the provided `TodoBoundary`.

        Args:
            todo_id (str): The ID of the task to update.
            todo_boundary (TodoBoundary): The new task details.

        Returns:
            Optional[TodoBoundary]: The updated task boundary object, or None if the task was not found.
        """
        loop = get_event_loop()

        def query_update_todo():
            todo_entity = self._todo_dao.query(TodoEntity).where(TodoEntity.id == todo_id).one_or_none()
            if not todo_entity:
                return

            todo_entity.update(todo_boundary.model_dump())
            self._todo_dao.add(todo_entity)
            self._todo_dao.commit()
            self._todo_dao.refresh(todo_entity)

            return TodoBoundary.from_entity(todo_entity)

        return await loop.run_in_executor(executor=None, func=query_update_todo)

    async def delete(self, todo_id: str) -> bool:
        """
        Delete a task from the database.

        This method searches for a task by its ID, and if found, deletes it from
        the database.

        Args:
            todo_id (str): The ID of the task to delete.

        Returns:
            bool: True if the task was successfully deleted, False if the task was not found.
        """
        loop = get_event_loop()

        def query_delete_todo():
            todo_entity = self._todo_dao.query(TodoEntity).where(TodoEntity.id == todo_id).one_or_none()
            if not todo_entity:
                return False

            self._todo_dao.delete(todo_entity)
            return True

        return await loop.run_in_executor(executor=None, func=query_delete_todo)
