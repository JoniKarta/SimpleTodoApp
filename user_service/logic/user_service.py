from asyncio import get_event_loop
from typing import Optional

from sqlalchemy.orm import Session

from common.models.token import Token
from common.utils.crypt_context import crypto_ctx
from common.utils.token_generator import create_access_token
from user_service.boundaries.user_boundary import UserBoundary
from user_service.boundaries.user_login import UserLogin
from user_service.boundaries.user_response import UserFilteredBoundary
from user_service.entities.user_entity import UserEntity
from user_service.logic.async_user_service import AsyncUserService


class UserService(AsyncUserService):
    """
    Service class that handles user authentication (login) and user registration
    operations asynchronously, interacting with the database through SQLAlchemy.

    Inherits from AsyncUserService to provide asynchronous capabilities for user
    management. This class allows the interaction with the user data access
    object (DAO) for querying users, verifying credentials, and creating new users
    while leveraging asynchronous execution to offload blocking operations like
    database queries.
    """

    def __init__(self):
        """
        Initializes the UserService instance.

        Sets up the initial state for the user DAO (`_user_dao`), which is used for
        database interactions. The `_user_dao` is initially set to `None` and is
        populated via the `set_user_dao` method via dependency injection.

        Attributes:
            _user_dao (Optional[Session]): The SQLAlchemy session used for database operations.
        """
        self._user_dao: Optional[Session] = None

    def set_user_dao(self, user_dao: Session) -> None:
        """
        Sets the SQLAlchemy session (`user_dao`) to be used by this service.

        This method allows external code to inject the database session (DAO) into
        the service, enabling the service to interact with the database.

        Args:
            user_dao (Session): An active SQLAlchemy session used for performing
                                 database operations.
        """
        self._user_dao = user_dao

    async def login(self, user_login: UserLogin) -> Optional[Token]:
        """
        Authenticates a user and returns a token if the login is successful.

        This method checks if the provided username and password match a record
        in the database. If the user is found and the password is verified,
        an access token is generated and returned. If the credentials are invalid,
        `None` is returned.

        Args:
            user_login (UserLogin): A boundary object containing the username and password
                                     to be used for authentication.

        Returns:
            Optional[Token]: An access token if authentication is successful, otherwise `None`.
        """
        loop = get_event_loop()

        def query_current_user():
            """
            Queries the database for the user by username and verifies the password.
            If valid, an access token is generated and returned.

            Returns:
                Token or None: A token if the user is found and the password is correct,
                               otherwise `None`.
            """
            user_entity = self._user_dao.query(UserEntity).where(
                UserEntity.username == user_login.username).one_or_none()
            if not user_entity or not crypto_ctx.verify(user_login.password, str(user_entity.hashed_password)):
                return None
            return create_access_token({'sub': user_entity.username})

        return await loop.run_in_executor(executor=None, func=query_current_user)

    async def register(self, user_boundary: UserBoundary) -> UserFilteredBoundary:
        """
        Registers a new user in the database.

        This method takes a `UserBoundary` object, converts it into a `UserEntity`,
        and saves it to the database. Upon successful registration, a `UserFilteredBoundary`
        object is returned with the newly created user data.

        Args:
            user_boundary (UserBoundary): A boundary object containing the user's data
                                           to be registered.

        Returns:
            UserFilteredBoundary: A boundary object containing the filtered user data
                                   after registration.
        """
        loop = get_event_loop()

        def register_user():
            """
            Converts the `user_boundary` to a `UserEntity`, adds it to the database,
            and commits the transaction. Returns a `UserFilteredBoundary` with the user data.
            """
            user_entity = UserEntity.from_boundary(user_boundary)
            self._user_dao.add(user_entity)
            self._user_dao.commit()
            return UserFilteredBoundary.from_entity(user_entity)

        return await loop.run_in_executor(executor=None, func=register_user)
