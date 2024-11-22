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
        return cls(**todo_entity.model_dump())
