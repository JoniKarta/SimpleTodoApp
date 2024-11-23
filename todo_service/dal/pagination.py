from typing import Literal, Any

from pydantic import BaseModel, Field

from todo_service.enums.attribute_types import AttributeTypes


class Pagination(BaseModel):
    page: int = Field(default=1, gt=0)
    size: int = Field(default=10, gt=0)
    order_by: Literal["title", "description", "status", "priority"] = "title"
    desc: bool = False

    def offset(self):
        return (self.page - 1) * self.size

class SearchByPagination(Pagination):
    search_type: AttributeTypes
    search_value: Any