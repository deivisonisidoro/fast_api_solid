from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import JWTError, jwt

from src.config.settings import Settings

from .interfaces.itoken_manager import ITokenManager


class TokenManager(ITokenManager):
    def __init__(self, settings=Settings()):
        self.settings = settings

    def create_access_token(self, data: dict) -> str:
        data = data.copy()
        expirations = datetime.utcnow() + timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRATION_MINUTES)
        data.update({"exp": expirations})
        token_jwt = jwt.encode(data, self.settings.SECRET_KEY, algorithm=self.settings.ALGORITHM)
        return token_jwt

    def generate_jwt_token(self, user_email: str) -> str:
        payload = {"email": user_email}
        print(self.settings)
        expirations = datetime.utcnow() + timedelta(minutes=5)
        # expirations = datetime.utcnow() + timedelta(minutes=self.settings.GENERAL_EXPIRES_IN_MINUTES)
        payload.update({"exp": expirations})
        encoded_jwt_token = jwt.encode(payload, self.settings.SECRET_KEY, algorithm=self.settings.ALGORITHM)
        return encoded_jwt_token

    def decode_jwt_token(self, encoded_jwt_token: str) -> dict[str, any]:
        try:
            decoded_jwt_token = jwt.decode(
                encoded_jwt_token, self.settings.SECRET_KEY, algorithms=[self.settings.ALGORITHM]
            )
            return decoded_jwt_token
        except JWTError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

    def verify_access_token(self, token: str) -> str:
        charge = jwt.decode(token, self.settings.SECRET_KEY, algorithms=[self.settings.ALGORITHM])
        return charge.get("sub")
