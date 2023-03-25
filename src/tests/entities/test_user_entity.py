import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.entities import User


class TestUserEntity:
    """A class to test the User entity."""

    def test_create_user(self, db: Session, user_data: dict):
        """Test creating a new User object and adding it to the database.

        Args:
            db (Session): A database session object.
            user_data (dict): A dictionary containing data for creating a new user.


        Expected Results:
            - A new User object is created with the provided data.
            - The object is added to the database.
            - The object has a non-null id attribute.
            - The object's name, email, and password attributes match the provided data.
        """

        # Test
        user = User(name=user_data["name"], email=user_data["email"], password=user_data["password"])
        db.add(user)
        db.commit()

        # Assert
        assert user.id is not None
        assert user.name == user_data["name"]
        assert user.email == user_data["email"]
        assert user.password == user_data["password"]

        # Cleanup
        db.rollback()

    def test_create_duplicate_user(self, db: Session, user_data: dict):
        """Test attempting to create a User object with a duplicate email.

        Args:
            db (Session): A database session object.
            user_data (dict): A dictionary containing data for creating a new user.

        Returns:
            None

        Expected Results:
            - A new User object is created with the provided data.
            - The object is added to the database.
            - An IntegrityError is raised when attempting to add a new User object with the same email.
        """

        # Create a user
        user = User(name=user_data["name"], email=user_data["email"], password=user_data["password"])
        db.add(user)
        db.commit()

        # Attempt to create a user with the same email
        with pytest.raises(IntegrityError):
            user2 = User(name=user_data["name"], email=user_data["email"], password=user_data["password"])
            db.add(user2)
            db.commit()
