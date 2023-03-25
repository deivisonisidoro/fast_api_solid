from pydantic import BaseModel, EmailStr

from .user_schema import UserOut


class LoginData(BaseModel):
    """
    Pydantic schema for login credentials.

    Attributes:
        email (EmailStr): Email of the user
        password (str): Password of the user
    """

    email: EmailStr
    password: str


class SuccessLogin(BaseModel):
    """
    Pydantic schema for successful login response.

    Attributes:
        user (UserOut): User object containing the user's details
        access_token (str): JWT access token for the user
    """

    user: UserOut
    access_token: str
