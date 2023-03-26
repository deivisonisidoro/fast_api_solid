from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.providers.token_manager_provider import TokenManagerProvider
from src.repositories.user_repository import UserRepository

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


class AuthenticationMiddleware:
    """
    Middleware that handles authentication for FastAPI endpoints.

    Attributes:
        oauth2_schema (OAuth2PasswordBearer): The OAuth2 password bearer object.
    """

    def verify_token(self, token: str):
        """
        Verify the JWT token and return the email address associated with it.

        Args:
            token (str): The JWT token to verify.

        Returns:
            email (str): The email address associated with the token, or None if the token is invalid.
        """
        try:
            email = TokenManagerProvider().verify_access_token(token)
        except JWTError:
            return None
        return email

    def get_user_by_email(self, email: str, db: Session):
        """
        Retrieve the user with the given email address from the database.

        Args:
            email (str): The email address of the user to retrieve.
            db (Session): The SQLAlchemy database session.

        Returns:
            user (User): The user with the given email address, or None if no such user exists.
        """
        return UserRepository(db).get_user_by_email(email)

    async def __call__(self, token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
        """
        Verify the JWT token and retrieve the user associated with it.

        Args:
            token (str, optional): The JWT token to verify. Defaults to Depends(oauth2_schema).
            db (Session, optional): The SQLAlchemy database session. Defaults to Depends(get_db).

        Raises:
            HTTPException: If the token is invalid or the user does not exist.

        Returns:
            user (User): The user associated with the JWT token.
        """
        email = self.verify_token(token)
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is not authorized")
        user = self.get_user_by_email(email, db)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
