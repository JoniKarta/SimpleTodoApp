from typing import Annotated
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from common.models.token import Token
from common.utils.crypt_context import crypto_ctx
from common.utils.token_generator import create_access_token
from todo_service.dal.todo_dao import get_todo_dao
from user_service.boundaries.user_boundary import UserBoundary
from user_service.boundaries.user_login import UserLogin
from user_service.boundaries.user_response import UserResponse
from user_service.entities.user_entity import UserEntity

router = APIRouter(
    prefix='/auth',
    tags=['User Routes']
)


@router.post('/register')
async def register(user_boundary: UserBoundary, db: Annotated[Session, Depends(get_todo_dao)]):
    try:
        user_entity = UserEntity.from_boundary(user_boundary)
        db.add(user_entity)
        db.commit()
        return UserResponse.from_entity(user_entity)
    except IntegrityError as e:
        str_ex = str(e.orig)
        if "unique constraint" in str_ex and "email" in str_ex:
            detail = "The email address is already taken."
        elif "unique constraint" in str_ex and "username" in str_ex:
            detail = "The username is already taken."
        elif "foreign key constraint" in str_ex:
            detail = "The provided foreign key value is invalid."
        else:
            detail = "An integrity error occurred. Please check your data."

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


@router.post('/login', response_model=Token)
async def login(user_login: UserLogin, db: Annotated[Session, Depends(get_todo_dao)]):
    user_entity = db.query(UserEntity).where(UserEntity.username == user_login.username).one_or_none()
    if not user_entity or not crypto_ctx.verify(user_login.password, str(user_entity.hashed_password)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    token = create_access_token({'sub': user_entity.username})
    return Token(access_token=token)


@router.post('/login/form', response_model=Token)
async def form_login(form: Annotated[OAuth2PasswordRequestForm, Depends()],
                     db: Annotated[Session, Depends(get_todo_dao)]):
    return await login(UserLogin(username=form.username, password=form.password), db)
