from datetime import datetime

from pydantic import BaseModel, EmailStr

from .user_schema import UserOut


class LoginData(BaseModel):
    email: EmailStr
    password: str


class SuccessLogin(BaseModel):
    user: UserOut
    access_token: str


class RefreshTokenData(BaseModel):
    refresh_token: str


class SuccessRefreshToken(BaseModel):
    access_token: str
