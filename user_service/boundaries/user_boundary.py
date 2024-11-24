from pydantic import BaseModel, Field, EmailStr


class UserBoundary(BaseModel):
    id: str = Field(default='')
    username: str = Field(min_length=3)
    email: EmailStr = Field(default='')
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    password: str