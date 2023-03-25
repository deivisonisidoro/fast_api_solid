from abc import ABC, abstractmethod
from typing import List

from fastapi import BackgroundTasks, Request

from src.schemas.user_schema import UserCreate, UserUpdate


class IUserService(ABC):
    """Interface for User Service.

    This interface defines the methods that should be implemented by any User Service class.

    """

    @abstractmethod
    def create_user(self, user: UserCreate) -> dict:
        """Create a new user.

        Args:
            user (UserCreate): User create schema.

        Returns:
            dict: User information.

        """

        pass

    @abstractmethod
    def get_user(self, user_id: int) -> dict:
        """Get a user by ID.

        Args:
            user_id (int): User ID.

        Returns:
            dict: User information.

        """

        pass

    @abstractmethod
    def list_users(self) -> List[dict]:
        """List all users.

        Returns:
            List[dict]: List of user information.

        """

        pass

    @abstractmethod
    def update_user(self, user_id: int, user_update: UserUpdate) -> dict:
        """Update a user.

        Args:
            user_id (int): User ID.
            user_update (UserUpdate): User update schema.

        Returns:
            dict: Updated user information.

        """

        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> dict:
        """Delete a user.

        Args:
            user_id (int): User ID.

        Returns:
            dict: Deleted user information.

        """

        pass

    @abstractmethod
    async def reset_password_request(self, email: str, request: Request, background_tasks: BackgroundTasks) -> dict:
        """Send a password reset email.

        Args:
            email (str): User email.
            request (Request): FastAPI request instance.
            background_tasks (BackgroundTasks): FastAPI background tasks instance.

        Returns:
            dict: Response message.

        """

        pass

    @abstractmethod
    def reset_password(self, token: str, password: str) -> dict:
        """Reset a user's password.

        Args:
            token (str): Password reset token.
            password (str): New password.

        Returns:
            dict: Response message.

        """

        pass
