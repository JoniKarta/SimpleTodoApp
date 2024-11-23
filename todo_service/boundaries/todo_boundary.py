from typing import Optional

from pydantic import BaseModel, Field

from todo_service.enums.todo_priority import Priority


class TodoBoundary(BaseModel):
    id: str
    title: str = Field(min_length=1)
    description: Optional[str] = ""
    status: str = "Pending"
    priority: Priority = Priority.LOW

    @classmethod
    def from_entity(cls, todo_entity: "TodoEntity") -> "TodoBoundary":
        return cls.model_validate({key: value for key, value in vars(todo_entity).items() if not key.startswith('_')})
