from pydantic import BaseModel, EmailStr

from .user_schema import UserOut


class LoginData(BaseModel):
    email: EmailStr
    password: str


class SuccessLogin(BaseModel):
    user: UserOut
    access_token: str
