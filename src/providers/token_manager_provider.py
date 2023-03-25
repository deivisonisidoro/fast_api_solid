from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import JWTError, jwt

from src.config.settings import Settings

from .interfaces.itoken_manager import ITokenManagerProvider


class TokenManagerProvider(ITokenManagerProvider):
    """
    TokenManagerProvider implements the ITokenManagerProvider interface to generate and verify access tokens.

    Args:
        settings (Settings): Settings object with the app's configuration.

    Attributes:
        settings (Settings): Settings object with the app's configuration.

    """

    def __init__(self, settings=Settings()):
        self.settings = settings

    def create_access_token(self, data: dict) -> str:
        """
        Create an access token with a given expiration time.

        Args:
            data (dict): Dictionary with the data to encode in the token.

        Returns:
            str: Encoded JWT token.

        """
        data = data.copy()
        expirations = datetime.utcnow() + timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRATION_MINUTES)
        data.update({"exp": expirations})
        token_jwt = jwt.encode(data, self.settings.SECRET_KEY, algorithm=self.settings.ALGORITHM)
        return token_jwt

    def generate_jwt_token(self, user_email: str) -> str:
        """
        Generate a JWT token with a given expiration time.

        Args:
            user_email (str): Email of the user to generate the token for.

        Returns:
            str: Encoded JWT token.

        """
        payload = {"email": user_email}
        expirations = datetime.utcnow() + timedelta(minutes=self.settings.GENERAL_EXPIRES_IN_MINUTES)
        payload.update({"exp": expirations})
        encoded_jwt_token = jwt.encode(payload, self.settings.SECRET_KEY, algorithm=self.settings.ALGORITHM)
        return encoded_jwt_token

    def decode_jwt_token(self, encoded_jwt_token: str) -> dict[str, any]:
        """
        Decode a JWT token.

        Args:
            encoded_jwt_token (str): Encoded JWT token to decode.

        Returns:
            dict: Decoded JWT token.

        Raises:
            HTTPException: If the token is invalid.

        """
        try:
            decoded_jwt_token = jwt.decode(
                encoded_jwt_token, self.settings.SECRET_KEY, algorithms=[self.settings.ALGORITHM]
            )
            return decoded_jwt_token
        except JWTError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

    def verify_access_token(self, token: str) -> str:
        """
        Verify if an access token is valid.

        Args:
            token (str): Access token to verify.

        Returns:
            str: User id encoded in the access token.

        """
        charge = jwt.decode(token, self.settings.SECRET_KEY, algorithms=[self.settings.ALGORITHM])
        return charge.get("sub")
