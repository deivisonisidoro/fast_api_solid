from dataclasses import dataclass

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.providers.password_manager_provider import PasswordManagerProvider
from src.providers.token_manager_provider import TokenManagerProvider
from src.repositories.interfaces.iuser_repository import IUserRepository
from src.repositories.user_repository import UserRepository
from src.schemas.login_schema import LoginData, SuccessLogin

from .interfaces.i_auth_services import IAuthService


@dataclass
class AuthService(IAuthService):
    """
    Implementation of the IAuthService interface for authentication.

    This class provides functionality for user authentication including verifying passwords and creating access tokens.

    Args:
        db: SQLAlchemy Session instance

    Attributes:
        db (Session): SQLAlchemy Session instance
        password_manager (PasswordManagerProvider): Password manager instance
        token_manager (TokenManagerProvider): Token manager instance
    """

    db: Session
    password_manager = PasswordManagerProvider()
    token_manager = TokenManagerProvider()

    def __post_init__(self):
        self._user_repository: IUserRepository = UserRepository(self.db)

    def login_for_access_token(self, login_data: LoginData) -> SuccessLogin:
        """
        Verifies user's email and password and returns a SuccessLogin object with an access token.

        Args:
            login_data (LoginData): User login data including email and password.

        Returns:
            SuccessLogin: A SuccessLogin object containing user data and access token.

        Raises:
            HTTPException: If the provided email or password is incorrect.
        """
        email = login_data.email
        password = login_data.password
        user = self._user_repository.get_user_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or password does not match",
            )
        valid_password = self.password_manager.hash_verify(password, user.password)

        if not valid_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or password does not match",
            )
        access_token = self.token_manager.create_access_token({"sub": user.email})
        return SuccessLogin(user=user, access_token=access_token)
