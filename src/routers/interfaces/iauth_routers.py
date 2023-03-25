from abc import ABC, abstractmethod

from src.schemas.login_schema import LoginData, SuccessLogin
from src.schemas.user_schema import UserIn
from src.services.interfaces.i_auth_services import IAuthService


class IAuthRouters(ABC):
    """
    Abstract base class for defining authentication related API routes."""

    @abstractmethod
    def login_for_access_token(self, login_data: LoginData, auth_service: IAuthService) -> SuccessLogin:
        """
        Abstract method for logging in a user and generating an access token.

        Args:
            login_data (LoginData):
                The user's email and password used for authentication.
            auth_service (IAuthService):
                An instance of the AuthService that will handle user authentication and access token generation.

        Returns:
            SuccessLogin:
                A schema representing a successful login attempt, containing a UserOut instance and an access token.
        """
        pass

    @abstractmethod
    def get_profile(user: UserIn):
        """
        Abstract method for getting a user's profile information.

        Args:
        -----
        user: UserIn
            The currently logged-in user.

        Returns:
        --------
        UserOut:
            A schema representing a user's profile information.
        """
        pass
