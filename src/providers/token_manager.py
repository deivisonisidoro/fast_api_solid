from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import JWTError, jwt

from .interfaces.itoken_manager import ITokenManager

SECRET_KEY = "key_secret"
ALGORITHM = "HS256"
ACCES_TOKEN_EXPIRES_IN_MINUTE = 3000
GENERAL_EXPIRES_IN_MINUTE = 2


class TokenManager(ITokenManager):
    def create_access_token(self, data: dict) -> str:
        data = data.copy()
        expirations = datetime.utcnow() + timedelta(minutes=ACCES_TOKEN_EXPIRES_IN_MINUTE)
        data.update({"exp": expirations})
        token_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        return token_jwt

    def generate_jwt_token(self, user_email: str) -> str:
        payload = {"email": user_email}
        expirations = datetime.utcnow() + timedelta(minutes=GENERAL_EXPIRES_IN_MINUTE)
        payload.update({"exp": expirations})
        encoded_jwt_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt_token

    def decode_jwt_token(self, encoded_jwt_token: str) -> dict[str, any]:
        try:
            decoded_jwt_token = jwt.decode(encoded_jwt_token, SECRET_KEY, algorithms=[ALGORITHM])
            return decoded_jwt_token
        except JWTError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

    def verify_access_token(self, token: str) -> str:
        charge = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return charge.get("sub")
