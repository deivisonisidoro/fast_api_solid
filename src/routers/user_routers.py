from dataclasses import dataclass
from typing import Dict, List

from fastapi import APIRouter, BackgroundTasks, Depends, Request, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.token_schema import TokenOut
from src.schemas.user_schema import PasswordReset, UserCreate, UserOut
from src.services.interfaces.i_user_services import IUserService
from src.services.user_service import UserService

from .interfaces.iuser_routers import IUserRouters

router = APIRouter()


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Dependency to get an instance of the UserService with the database session provided by the get_db function.

    Args:
        db (Session): The database session.

    Returns:
        UserService: An instance of the UserService.
    """
    return UserService(db)


@dataclass
class UserRouters(IUserRouters):
    """Implements the IUserRouters interface and defines the endpoints for User-related operations.

    Args:
        IUserController (Interface): The IUserRouters interface that this class is implementing.
    """

    @staticmethod
    @router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
    def create_user(user_create: UserCreate, user_service: IUserService = Depends(get_user_service)) -> UserOut:
        """Endpoint to create a new user.

        Args:
            user_create (UserCreate): The UserCreate object that represents the user to be created.
            user_service (IUserService): The UserService instance that will handle the creation of the user.

        Returns:
            UserOut: The UserOut object representing the user that was created.
        """
        return user_service.create_user(user_create)

    @staticmethod
    @router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
    def get_user(user_id: int, user_service: IUserService = Depends(get_user_service)) -> UserOut:
        """Endpoint to retrieve a user by its ID.

        Args:
            user_id (int): The ID of the user to be retrieved.
            user_service (IUserService): The UserService instance that will handle the retrieval of the user.

        Returns:
            UserOut: The UserOut object representing the user that was retrieved.
        """
        return user_service.get_user(user_id)

    @staticmethod
    @router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserOut])
    def list_users(user_service: IUserService = Depends(get_user_service)) -> List[UserOut]:
        """Endpoint to retrieve all users.

        Args:
            user_service (IUserService): The UserService instance that will handle the retrieval of the users.

        Returns:
            List[UserOut]: A list of UserOut objects representing all users in the database.
        """
        return user_service.list_users()

    @staticmethod
    @router.patch("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
    def update_user(user_service: IUserService = Depends(get_user_service)) -> UserOut:
        """Endpoint to update a user by its ID.

        Args:
            user_service (IUserService): The UserService instance that will handle the update of the user.

        Returns:
            UserOut: The UserOut object representing the user that was updated.
        """
        return user_service.update_user

    @staticmethod
    @router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_user(user_id: int, user_service: IUserService = Depends(get_user_service)):
        """Deletes a user by its ID.

        Args:
            user_id: The ID of the user to delete.
            user_service: The service instance to use to delete the user.

        Returns:
            A dictionary containing a message indicating that the user was deleted successfully.
        """
        user_service.delete_user(user_id)
        return {"detail": "User deleted successfully"}

    @staticmethod
    @router.post("/password-reset-request", status_code=status.HTTP_200_OK)
    async def reset_password_request(
        email: str,
        request: Request,
        background_tasks: BackgroundTasks,
        user_service: IUserService = Depends(get_user_service),
    ) -> Dict[str, str]:
        """Initiates the password reset process for a user.

        Args:
            email: The email address of the user requesting the password reset.
            request: The request object used to initiate the password reset.
            background_tasks: The background tasks instance used to send the password reset email asynchronously.
            user_service: The service instance to use to initiate the password reset.

        Returns:
            A dictionary containing a message indicating that the password reset process has started.
        """
        return await user_service.reset_password_request(email, request, background_tasks)

    @staticmethod
    @router.post("/password-reset", status_code=status.HTTP_200_OK, response_model=TokenOut)
    async def password_reset(
        password_reset: PasswordReset, user_service: IUserService = Depends(get_user_service)
    ) -> Dict[str, str]:
        """Resets a user's password.

        Args:
            password_reset: The object containing the token and new password to set.
            user_service: The service instance to use to reset the password.

        Returns:
            A dictionary containing a message indicating that the password was reset successfully.
        """
        return user_service.reset_password(password_reset)
