from datetime import datetime, timedelta

from jose import jwt

from .interfaces.itoken_manager import ITokenManager

SECRET_KEY = "key_secret"
ALGORITHM = "HS256"
EXPIRES_IN_MINUTE = 3000


class TokenManager(ITokenManager):
    def create_access_token(self, data: dict) -> str:
        data = data.copy()
        expirations = datetime.utcnow() + timedelta(minutes=EXPIRES_IN_MINUTE)
        data.update({"exp": expirations})
        token_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        return token_jwt

    def verify_access_token(self, token: str) -> str:
        charge = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return charge.get("sub")
