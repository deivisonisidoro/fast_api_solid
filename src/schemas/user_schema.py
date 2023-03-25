from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """
    Pydantic schema representing the base user attributes.

    Attributes:
        name (str): The user's name
        email (EmailStr): The user's email address
    """

    name: str
    email: EmailStr


class UserCreate(UserBase):
    """
    Pydantic schema representing the attributes required to create a user.

    Inherits from UserBase.

    Attributes:
        password (str): The user's password
    """

    password: str


class UserUpdate(UserBase):
    """
    Pydantic schema representing the attributes that can be updated for a user.

    Inherits from UserBase.

    Attributes:
        password (Optional[str]): The user's password (optional)
    """

    password: Optional[str]


class UserIn(UserBase):
    """
    Pydantic schema representing the attributes required to log a user in.

    Inherits from UserBase.

    Attributes:
        password (str): The user's password
    """

    password: str


class UserOut(UserBase):
    """
    Pydantic schema representing the attributes returned for a user.

    Inherits from UserBase.

    Attributes:
        id (int): The user's ID
        created_at (datetime): The date and time when the user was created

    Config:
        orm_mode (bool): Whether or not the model is being used in an ORM mode
    """

    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PasswordReset(BaseModel):
    """
    Pydantic schema representing the attributes required to reset a user's password.

    Attributes:
        email (str): The user's email address
        password (str): The user's new password
        token (str): The reset token sent to the user's email
    """

    email: str
    password: str
    token: str


class UserDB(UserBase):
    """
    Pydantic schema representing a user stored in the database.

    Inherits from UserBase.

    Attributes:
        id (int): The user's ID
        password (str): The user's hashed password
        created_at (datetime): The date and time when the user was created

    Config:
        orm_mode (bool): Whether or not the model is being used in an ORM mode
    """

    id: int
    password: str
    created_at: datetime

    class Config:
        orm_mode = True
