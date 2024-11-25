from typing import Optional

from pydantic import Field

from user_service.boundaries.user_boundary import UserBoundary


class UserFilteredBoundary(UserBoundary):
    password: Optional[str] = Field(exclude=True)

    @classmethod
    def from_entity(cls, user_entity: "UserEntity") -> "UserFilteredBoundary":
        return cls(
            id=user_entity.id,
            username=user_entity.username,
            email=user_entity.email,
            first_name=user_entity.first_name,
            last_name=user_entity.last_name,
            password=None
        )
