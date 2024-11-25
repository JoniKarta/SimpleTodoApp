from typing import Annotated, Callable, Dict

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from configuration.config import Config
from todo_service.boundaries.todo_boundary import TodoBoundary
from todo_service.dal.pagination import Pagination, SearchByPagination
from todo_service.enums.attribute_types import AttributeTypes
from todo_service.logic.async_todo_service import AsyncTodoService
from todo_service.logic.mock_todo_service import MockTodoService
from todo_service.logic.todo_service import TodoService

config = Config()

if config.DEV_ENVIRONMENT:
    from todo_service.dal.mock_todo_dao import get_todo_dao
else:
    from todo_service.dal.todo_dao import get_todo_dao

router = APIRouter(tags=["Todo Routes"])


def get_todo_service(todo_dao: Annotated[Session, Depends(get_todo_dao)]) -> AsyncTodoService:
    todo_service = MockTodoService() if config.DEV_ENVIRONMENT else TodoService()
    todo_service.set_todo_dao(todo_dao)
    return todo_service


@router.get("/todos", status_code=HTTP_200_OK)
async def get_all_todos(
        pagination_query: Annotated[Pagination, Query()],
        todo_service: Annotated[AsyncTodoService, Depends(get_todo_service)]
):
    return await todo_service.get_all_todos(pagination_query)


@router.get("/todos/attribute_type", status_code=HTTP_200_OK)
async def get_todo_by_attribute(
        pagination_query: Annotated[SearchByPagination, Query()],
        todo_service: Annotated[AsyncTodoService, Depends(get_todo_service)],
):
    method_map: Dict[AttributeTypes, Callable] = {
        AttributeTypes.ID: todo_service.get_todo_by_id,
        AttributeTypes.TITLE: todo_service.get_todo_by_title,
        AttributeTypes.PRIORITY: todo_service.get_todo_by_priority,
    }
    attr_type = pagination_query.search_type
    attr_value = pagination_query.search_value
    method = method_map.get(attr_type)
    if not method:
        raise HTTPException(
            HTTP_400_BAD_REQUEST,
            detail=f"The attribute type '{attr_type}' is not supported. "
                   "Please use one of the following: ID, TITLE, or PRIORITY.",
        )

    try:
        ret_value = await method(attr_value, pagination_query)
    except ValueError as err:
        raise HTTPException(
            HTTP_400_BAD_REQUEST,
            detail=f"Invalid input for attribute value: {attr_value}. {str(err)}",
        )

    if ret_value is None:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail=f"No task found matching {attr_type.value.lower()}='{attr_value}'.",
        )

    return ret_value


@router.post("/todos", status_code=HTTP_201_CREATED)
async def create_task(
        todo_boundary: TodoBoundary,
        todo_service: Annotated[AsyncTodoService, Depends(get_todo_service)],
):
    return await todo_service.create_todo(todo_boundary)


@router.put("/todos/{todo_id}", status_code=HTTP_200_OK)
async def update_task(
        todo_id: str,
        todo_boundary: TodoBoundary,
        todo_service: Annotated[AsyncTodoService, Depends(get_todo_service)],
):
    updated_todo = await todo_service.update_todo(todo_id, todo_boundary)
    if not updated_todo:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail=f"Task with ID '{todo_id}' not found. "
                   "Please ensure the task exists before attempting an update.",
        )
    return updated_todo


@router.delete("/todos/{todo_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_task(
        todo_id: str,
        todo_service: Annotated[AsyncTodoService, Depends(get_todo_service)],
):
    if not await todo_service.delete(todo_id):
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail=f"Task with ID '{todo_id}' not found. "
                   "Unable to delete a non-existing task.",
        )
