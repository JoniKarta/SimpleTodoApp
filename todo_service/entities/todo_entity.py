import uuid
from typing import Dict, Any

from sqlalchemy import String, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

from todo_service.enums.todo_priority import Priority

Base = declarative_base()


class TodoEntity(Base):
    __tablename__ = "todos"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    status: Mapped[str] = mapped_column(String())
    priority: Mapped[Priority] = mapped_column(Enum(Priority))

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
