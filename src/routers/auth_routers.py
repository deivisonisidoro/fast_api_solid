from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.login_schema import LoginData, SuccessLogin
from src.schemas.user_schema import UserIn, UserOut
from src.services.auth_service import AuthService
from src.services.interfaces.i_auth_services import IAuthService
from src.utils.auths_utils import get_user_logged_in

from .interfaces.iauth_routers import IAuthRouters

router = APIRouter()


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """
    Get an instance of the AuthService with the database session provided by the get_db function.

    Args:
        db (Session): The SQLAlchemy database session provided by the get_db function.

    Returns:
        AuthService: An instance of the AuthService class.
    """
    return AuthService(db)


class AuthRouters(IAuthRouters):
    """
    Class containing endpoints related to user authentication.
    """

    @staticmethod
    @router.post("/token", status_code=status.HTTP_200_OK, response_model=SuccessLogin)
    def login_for_access_token(
        login_data: LoginData,
        auth_service: IAuthService = Depends(get_auth_service),
    ) -> SuccessLogin:
        """
        Log in a user and generate an access token.

        Args:
            login_data (LoginData): The user's email and password used for authentication.
            auth_service (IAuthService): The AuthService instance that will handle user authentication and access token generation.

        Returns:
            SuccessLogin: A schema representing a successful login attempt, containing a UserOut instance and an access token.
        """
        return auth_service.login_for_access_token(login_data)

    @staticmethod
    @router.get("/profile", status_code=status.HTTP_200_OK, response_model=UserOut)
    async def get_profile(user: UserIn = Depends(get_user_logged_in)):
        """
        Get a user's profile information.

        Args:
            user (UserIn): The currently logged-in user.

        Returns:
            UserOut: A schema representing a user's profile information.
        """
        return user
