from abc import ABC, abstractmethod
from typing import Any, List

from fastapi import BackgroundTasks, Request

from src.schemas.token_schema import TokenOut
from src.schemas.user_schema import PasswordReset, UserCreate, UserOut, UserUpdate
from src.services.interfaces.i_user_services import IUserService


class IUserRouters(ABC):
    """
    Interface for user-related routers. All routers should implement this interface.
    """

    @abstractmethod
    def create_user(self, user: UserCreate, user_service: IUserService) -> UserOut:
        """
        Abstract method to create a new user.

        Args:
            user (UserCreate): The UserCreate object representing the user to be created.
            user_service (IUserService): The UserService instance that will handle the creation of the user.

        Returns:
            UserOut: The UserOut object representing the user that was created.
        """
        pass

    @abstractmethod
    def get_user(self, user_id: int, user_service: IUserService) -> UserOut:
        """
        Abstract method to retrieve a user by its ID.

        Args:
            user_id (int): The ID of the user to be retrieved.
            user_service (IUserService): The UserService instance that will handle the retrieval of the user.

        Returns:
            UserOut: The UserOut object representing the user that was retrieved.
        """
        pass

    @abstractmethod
    def list_users(self, user_service: IUserService) -> List[UserOut]:
        """
        Abstract method to retrieve a list of all users.

        Args:
            user_service (IUserService): The UserService instance that will handle the retrieval of the list of users.

        Returns:
            List[UserOut]: A list of UserOut objects representing all users.
        """
        pass

    @abstractmethod
    def update_user(self, user_id: int, user_update: UserUpdate, user_service: IUserService) -> UserOut:
        """
        Abstract method to update a user by its ID.

        Args:
            user_id (int): The ID of the user to be updated.
            user_update (UserUpdate): The UserUpdate object that represents the changes to be made to the user.
            user_service (IUserService): The UserService instance that will handle the update of the user.

        Returns:
            UserOut: The UserOut object representing the user that was updated.
        """
        pass

    @abstractmethod
    def delete_user(self, user_id: int, user_service: IUserService) -> Any:
        """
        Abstract method to delete a user by its ID.

        Args:
            user_id (int): The ID of the user to be deleted.
            user_service (IUserService): The UserService instance that will handle the deletion of the user.

        Returns:
            Any: A dictionary containing a message indicating that the user was deleted successfully.
        """
        pass

    @abstractmethod
    def reset_password_request(
        self, email: str, request: Request, background_tasks: BackgroundTasks, user_service: IUserService
    ):
        """
        Abstract method to initiate the password reset process for a user.

        Args:
            email (str): The email address of the user requesting the password reset.
            request (Request): The request object used to initiate the password reset.
            background_tasks (BackgroundTasks): The background tasks instance used to send the password reset email asynchronously.
            user_service (IUserService): The UserService instance that will handle the password reset request.

        Returns:
            Any: A dictionary containing a message indicating that the password reset process has started.
        """
        pass

    @abstractmethod
    def password_reset(password_reset: PasswordReset, user_service: IUserService) -> TokenOut:
        """Abstract method to reset a user's password.

        Args:
            password_reset (PasswordReset): The PasswordReset object containing the new password and a reset token.
            user_service (IUserService): The IUserService instance that will handle the password reset.

        Returns:
            TokenOut: The TokenOut object containing a new access token.
        """
        pass
