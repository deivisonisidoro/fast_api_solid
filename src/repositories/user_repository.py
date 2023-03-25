from typing import List, Optional

from sqlalchemy.orm import Session

from src.entities.user_entity import User
from src.providers.password_manager_provider import PasswordManagerProvider
from src.schemas.user_schema import UserCreate, UserUpdate

from .interfaces.iuser_repository import IUserRepository


class UserRepository(IUserRepository):
    """Implementation of the IUserRepository interface for User entity.

    This class handles database interactions with the User entity, including creating, reading, updating, and deleting
    User records.

    Args:
        db: SQLAlchemy Session instance
        password_manager: Password manager instance, defaults to None

    Attributes:
        db (Session): SQLAlchemy Session instance
        password_manager (Optional[PasswordManagerProvider]): Password manager instance, defaults to None
    """

    def __init__(
        self,
        db: Session,
        password_manager: Optional[PasswordManagerProvider] = None,
    ) -> None:
        """Constructor method to initialize UserRepository instance.

        Args:
            db (Session): SQLAlchemy Session instance
            password_manager (Optional[PasswordManagerProvider], optional): Password manager instance, defaults to None
        """
        self.db = db
        self.password_manager = password_manager if password_manager else PasswordManagerProvider()

    def create_user(self, user: UserCreate) -> User:
        """Create a new User entity.

        Args:
            user (UserCreate): User create schema.

        Returns:
            User: User entity.
        """
        user.password = self.password_manager.hash_generate(user.password)
        db_user = User(name=user.name, email=user.email, password=user.password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_by_id(self, user_id: int) -> User:
        """Retrieve a User entity by id.

        Args:
            user_id (int): User id.

        Returns:
            User: User entity.
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> User:
        """Retrieve a User entity by email.

        Args:
            email (str): User email.

        Returns:
            User: User entity.
        """
        return self.db.query(User).filter(User.email == email).first()

    def get_all_users(self) -> List[User]:
        """Retrieve all User entities.

        Returns:
            List[User]: List of User entities.
        """
        return self.db.query(User).all()

    def update_user(self, user: User, user_update: UserUpdate) -> User:
        """Update a User entity.

        Args:
            user (User): User entity to update.
            user_update (UserUpdate): User update schema.

        Returns:
            User: Updated User entity.
        """
        user.name = user_update.name or user.name
        user.email = user_update.email or user.email

        if user_update.password:
            user.password = self.password_manager.hash_generate(user_update.password)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user_password(self, user: User, password: str) -> User:
        """Update the password of a User entity.

        Args:
            user (User): User entity to update.
            password (str): New password.

        Returns:
            User: Updated User entity.
        """
        user.password = self.password_manager.hash_generate(password)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user: User) -> None:
        """
        Deletes a User entity from the database.

        Args:
            user (User): The User entity to be deleted.

        Returns:
            None
        """
        self.db.delete(user)
        self.db.commit()
