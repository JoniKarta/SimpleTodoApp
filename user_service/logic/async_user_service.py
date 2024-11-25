from abc import ABC, abstractmethod
from typing import Optional

from common.models.token import Token
from user_service.boundaries.user_boundary import UserBoundary
from user_service.boundaries.user_login import UserLogin
from user_service.boundaries.user_response import UserFilteredBoundary


class AsyncUserService(ABC):

    @abstractmethod
    async def login(self, user_login: UserLogin) -> Optional[Token]:
        ...

    @abstractmethod
    async def register(self, user_boundary: UserBoundary) -> Optional[UserFilteredBoundary]:
        ...
