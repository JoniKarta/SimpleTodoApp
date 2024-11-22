import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from common.database.base import Base
from common.utils.crypt_context import crypto_ctx


class UserEntity(Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(String(128), primary_key=True, default=lambda: str(uuid.uuid4()))
    username: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str] = mapped_column(String(64))
    hashed_password: Mapped[str] = mapped_column(String(64), unique=True)

    @classmethod
    def from_boundary(cls, user_boundary: "UserBoundary") -> "UserEntity":
        user_entity = cls()
        user_entity.username = user_boundary.username
        user_entity.email = user_boundary.email
        user_entity.first_name = user_boundary.first_name
        user_entity.last_name = user_boundary.last_name
        user_entity.hashed_password = crypto_ctx.hash(user_boundary.password)
        return user_entity
