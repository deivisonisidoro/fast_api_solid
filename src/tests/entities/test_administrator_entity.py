from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.entities.administrator_entity import Administrator
from src.entities.user_entity import User


class TestAdministratorEntity:
    """A class to test the Administrator entity."""

    def test_create_admin_user(self, db: Session, user_data: dict):
        """Test creating a new Administrator object and adding it to the database.

        Args:
            db (Session): A database session object.
            user_data (dict): A dictionary containing data for creating a new user.

        Returns:
            None

        Expected Results:
            - A new User object is created with the provided data.
            - The User object is added to the database.
            - A new Administrator object is created with the User object as its user attribute.
            - The Administrator object is added to the database.
            - The Administrator object has a non-null id attribute.
            - The Administrator object's user_id attribute matches the User object's id attribute.
        """

        # Create a User object
        user = User(name=user_data["name"], email=user_data["email"], password=user_data["password"])
        db.add(user)
        db.commit()

        # Create an Administrator object with the User object as its user attribute
        admin = Administrator(user=user)
        db.add(admin)
        db.commit()

        # Assert
        assert admin.id is not None
        assert admin.user_id == user.id

    def test_administrator_uniqueness(self, db: Session, user_data: dict):
        """Test attempting to create two Administrator objects with the same User object.

        Args:
            db (Session): A database session object.
            user_data (dict): A dictionary containing data for creating a new user.

        Returns:
            None

        Expected Results:
            - A new User object is created with the provided data.
            - The User object is added to the database.
            - An IntegrityError is raised when attempting to add two Administrator objects with the same User object.
        """

        # Create a User object
        user = User(name=user_data["name"], email=user_data["email"], password=user_data["password"])
        db.add(user)
        db.commit()

        # Attempt to create two Administrator objects with the same User object
        with pytest.raises(IntegrityError):
            admin1 = Administrator(user=user)
            admin2 = Administrator(user=user)
            db.add_all([admin1, admin2])
            db.commit()
