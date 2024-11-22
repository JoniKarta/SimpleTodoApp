from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from common.models.token import Token
from user_service.boundaries.user_boundary import UserBoundary
from user_service.boundaries.user_login import UserLogin
from user_service.dal.user_dao import get_user_dao
from user_service.logic.user_service import UserService

router = APIRouter(
    prefix='/auth',
    tags=['User Routes']
)


def get_user_service(user_dao: Annotated[Session, Depends(get_user_dao)]):
    user_service = UserService()
    user_service.set_user_dao(user_dao)
    return user_service


@router.post('/register')
async def register(user_boundary: UserBoundary, user_service: Annotated[UserService, Depends(get_user_service)]):
    try:
        return await user_service.register(user_boundary)
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
async def login(user_login: UserLogin, user_service: Annotated[UserService, Depends(get_user_service)]):
    token = await user_service.login(user_login)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    return Token(access_token=token)


@router.post('/login/form', response_model=Token)
async def form_login(form: Annotated[OAuth2PasswordRequestForm, Depends()],
                     user_service: Annotated[UserService, Depends(get_user_service)]):
    return await login(UserLogin(username=form.username, password=form.password), user_service)
