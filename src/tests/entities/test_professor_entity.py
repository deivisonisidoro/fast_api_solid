import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.entities.professor_entity import Professor
from src.entities.user_entity import User


class TestProfessorEntity:
    """
    A class to test the Professor entity.

    """

    def test_create_professor_user(self, db: Session, user_data: dict):
        """Test creating a new Professor object and adding it to the database.

        Args:
            db (Session): A database session object.
            user_data (dict): A dictionary containing data for creating a new user.

        Expected Results:
            - A new Professor object is created with the provided data.
            - The object is added to the database.
            - The object has a non-null id attribute.
            - The object's user_id attribute matches the id of the provided user object.
        """

        # Test
        user = User(name=user_data["name"], email=user_data["email"], password=user_data["password"])
        db.add(user)
        db.commit()

        professor = Professor(user=user)
        db.add(professor)
        db.commit()

        # Assert
        assert professor.id is not None
        assert professor.user_id == user.id

        # Cleanup
        db.rollback()

    def test_professor_uniqueness(self, db: Session, user_data: dict):
        """Test attempting to create a Professor object with a duplicate user.

        Args:
            db (Session): A database session object.
            user_data (dict): A dictionary containing data for creating a new user.

        Returns:
            None

        Expected Results:
            - A new Professor object is created with the provided data.
            - The object is added to the database.
            - An IntegrityError is raised when attempting to add a new Professor object with the same user.
        """

        # Create a user
        user = User(name=user_data["name"], email=user_data["email"], password=user_data["password"])
        db.add(user)
        db.commit()

        # Attempt to create a professor with the same user
        with pytest.raises(IntegrityError):
            professor1 = Professor(user=user)
            professor2 = Professor(user=user)
            db.add_all([professor1, professor2])
            db.commit()
