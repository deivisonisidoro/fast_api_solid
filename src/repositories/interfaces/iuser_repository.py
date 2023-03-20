from abc import ABC, abstractmethod
from typing import List

from src.entities.user_entity import User
from src.schemas.user_schema import UserCreate, UserUpdate


class IUserRepository(ABC):
    """
    An abstract base class that defines the interface for a repository responsible for managing user entities in a data store.

    Concrete implementations of this interface will provide the necessary functionality to interact with a specific data store.

    Attributes:
        ABC (class): A helper class that has ABCMeta as its metaclass. With this class, an abstract base class can be defined by simply deriving from ABC avoiding sometimes-confusing metaclass usage.

    Methods:
        create_user(user: UserCreate) -> User:
            Creates a new user entity and returns it after persisting it to the data store.

        get_user_by_id(user_id: int) -> User:
            Retrieves a user entity by its unique identifier from the data store.

        get_user_by_email(email: str) -> User:
            Retrieves a user entity by its email address from the data store.

        get_all_users() -> List[User]:
            Retrieves all user entities from the data store.

        update_user(user: User, user_update: UserUpdate) -> User:
            Updates an existing user entity and returns it after persisting the changes to the data store.

        update_user_password(user: User, password: str) -> User:
            Updates the password of an existing user entity and returns it after persisting the changes to the data store.

        delete_user(user: User):
            Deletes an existing user entity from the data store.
    """

    @abstractmethod
    def create_user(self, user: UserCreate) -> User:
        """
        Creates a new user entity and returns it after persisting it to the data store.

        Args:
            user (UserCreate): A `UserCreate` object containing the user's details.

        Returns:
            A `User` object representing the newly created user entity.
        """
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        """
        Retrieves a user entity by its unique identifier from the data store.

        Args:
            user_id (int): An integer representing the unique identifier of the user entity.

        Returns:
            A `User` object representing the retrieved user entity.

        Raises:
            `ValueError` if the specified user ID does not exist in the data store.
        """
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        """
        Retrieves a user entity by its email address from the data store.

        Args:
            email (str): A string representing the email address of the user entity.

        Returns:
            A `User` object representing the retrieved user entity.

        Raises:
            `ValueError` if the specified email address does not exist in the data store.
        """
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        """
        Retrieves all user entities from the data store.

        Returns:
            A list of `User` objects representing all user entities in the data store.
        """
        pass

    @abstractmethod
    def update_user(self, user: User, user_update: UserUpdate) -> User:
        """
        Updates an existing user entity and returns it after persisting the changes to the data store.

        Args:
            user (User): A `User` object representing the existing user entity to update.
            user_update (UserUpdate): A `UserUpdate` object containing the updated user details.

        Returns:
            A `User`
        """

    @abstractmethod
    def update_user_password(self, user: User, password: str) -> User:
        """
        Updates the password of an existing user entity and returns it after persisting the changes to the data store.

        Args:
            user (User): A `User` object representing the existing user entity to update.
            password (str): A string representing the updated password.

        Returns:
            A `User` object representing the updated user entity.
        """
        pass

    @abstractmethod
    def delete_user(self, user: User):
        """
        Deletes an existing user entity from the data store.

        Args:
            user (User): A `User` object representing the existing user entity to delete.
        """
        pass
