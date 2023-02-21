from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str]


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PasswordReset(BaseModel):
    email: str
    password: str
    token: str


class UserDB(UserBase):
    id: int
    password: str
    created_at: datetime

    class Config:
        orm_mode = True
