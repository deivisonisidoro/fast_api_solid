from pydantic import BaseModel


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RefreshTokenData(BaseModel):
    refresh_token: str


class SuccessRefreshToken(BaseModel):
    access_token: str
