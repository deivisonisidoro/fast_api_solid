from pydantic import BaseModel


class TokenOut(BaseModel):
    """
    Pydantic schema for JWT token response.

    Attributes:
        access_token (str): JWT access token for the user
        token_type (str): Type of the JWT token (default: "bearer")
    """

    access_token: str
    token_type: str = "bearer"


class RefreshTokenData(BaseModel):
    """
    Pydantic schema for refresh token data.

    Attributes:
        refresh_token (str): Refresh token for generating new JWT tokens
    """

    refresh_token: str


class SuccessRefreshToken(BaseModel):
    """
    Pydantic schema for successful refresh token response.

    Attributes:
        access_token (str): New JWT access token
    """

    access_token: str
