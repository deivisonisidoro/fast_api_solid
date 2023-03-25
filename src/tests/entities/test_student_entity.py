import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.entities.students_entity import Student
from src.entities.user_entity import User


class TestStudentEntity:
    """A class to test the Student entity."""

    def test_create_student_user(self, db: Session, user_data: dict):
        """Test creating a new Student object with an associated User object and adding it to the database.

        Args:
            db (Session): A database session object.
            user_data (dict): A dictionary containing data for creating a new user.

        Returns:
            None

        Expected Results:
            - A new User object is created with the provided data.
            - The User object is added to the database.
            - A new Student object is created with the User object as its user attribute.
            - The Student object is added to the database.
            - The Student object has a non-null id attribute.
            - The Student object's user_id attribute matches the id of the associated User object.
        """

        user = User(name=user_data["name"], email=user_data["email"], password=user_data["password"])
        db.add(user)
        db.commit()

        student = Student(user=user)
        db.add(student)
        db.commit()
        assert student.id is not None
        assert student.user_id == user.id

    def test_student_uniqueness(self, db: Session, user_data: dict):
        """Test attempting to create two Student objects with the same User object.

        Args:
            db (Session): A database session object.
            user_data (dict): A dictionary containing data for creating a new user.

        Returns:
            None

        Expected Results:
            - A new User object is created with the provided data.
            - The User object is added to the database.
            - An IntegrityError is raised when attempting to add two Student objects with the same User object.
        """

        user = User(name=user_data["name"], email=user_data["email"], password=user_data["password"])
        db.add(user)
        db.commit()

        with pytest.raises(IntegrityError):
            student1 = Student(user=user)
            student2 = Student(user=user)
            db.add_all([student1, student2])
            db.commit()
