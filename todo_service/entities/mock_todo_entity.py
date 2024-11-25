import uuid
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field

from todo_service.enums.todo_priority import Priority


class MockTodoEntity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: Optional[str] = ""
    status: str = "Pending"
    priority: Priority = Priority.LOW

    @classmethod
    def from_boundary(cls, todo_boundary: "TodoBoundary") -> "TodoEntity":
        model = cls()
        model.title = todo_boundary.title
        model.description = todo_boundary.description
        model.status = todo_boundary.status
        model.priority = todo_boundary.priority
        return model

    def update(self, data: Dict[str, Any]) -> None:
        data.pop('id', None)
        for field, value in data.items():
            setattr(self, field, value)

