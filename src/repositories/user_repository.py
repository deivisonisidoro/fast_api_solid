from typing import List, Optional

from sqlalchemy.orm import Session

from src.entities.user_entity import User
from src.providers.password_manager_provider import PasswordManagerProvider
from src.schemas.user_schema import UserCreate, UserUpdate

from .interfaces.iuser_repository import IUserRepository


class UserRepository(IUserRepository):
    """
    Implementation of the IUserRepository interface for User entity.
    This class handles database interactions with the User entity, including creating, reading, updating, and deleting
    User records.

    :param db: SQLAlchemy Session instance
    :type db: Session
    :param password_manager: Password manager instance, defaults to None
    :type password_manager: Optional[PasswordManagerProvider], optional
    """

    def __init__(
        self,
        db: Session,
        password_manager: Optional[PasswordManagerProvider] = None,
    ):
        """
        Constructor method to initialize UserRepository instance

        :param db: SQLAlchemy Session instance
        :type db: Session
        :param password_manager: Password manager instance, defaults to None
        :type password_manager: Optional[PasswordManagerProvider], optional
        """
        self.db = db
        self.password_manager = password_manager if password_manager else PasswordManagerProvider()

    def create_user(self, user: UserCreate) -> User:
        """
        Create a new User entity

        :param user: User create schema
        :type user: UserCreate
        :return: User entity
        :rtype: User
        """
        user.password = self.password_manager.hash_generate(user.password)
        db_user = User(name=user.name, email=user.email, password=user.password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_by_id(self, user_id: int) -> User:
        """
        Retrieve a User entity by id

        :param user_id: User id
        :type user_id: int
        :return: User entity
        :rtype: User
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> User:
        """
        Retrieve a User entity by email

        :param email: User email
        :type email: str
        :return: User entity
        :rtype: User
        """
        return self.db.query(User).filter(User.email == email).first()

    def get_all_users(self) -> List[User]:
        """
        Retrieve all User entities

        :return: List of User entities
        :rtype: List[User]
        """
        return self.db.query(User).all()

    def update_user(self, user: User, user_update: UserUpdate) -> User:
        """
        Update a User entity

        :param user: User entity to update
        :type user: User
        :param user_update: User update schema
        :type user_update: UserUpdate
        :return: Updated User entity
        :rtype: User
        """
        user.name = user_update.name or user.name
        user.email = user_update.email or user.email

        if user_update.password:
            user.password = self.password_manager.hash_generate(user_update.password)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user_password(self, user: User, password: str) -> User:
        """
        Update the password of a User entity

        :param user: User entity to update
        :type user: User
        :param password: New password
        :type password: str
        :return: Updated User entity
        :rtype: User
        """
        user.password = self.password_manager.hash_generate(password)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user: User):
        """
        Delete a User entity

        :param user: User entity to delete
        :type user: User
        """
        self.db.delete(user)
        self.db.commit()
