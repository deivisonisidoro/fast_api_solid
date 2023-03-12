import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.entities.students_entity import Student
from src.entities.user_entity import User


class TestStudentEntity:
    def test_create_student_user(self, db: Session, user_data: dict):
        user = User(name=user_data["name"], email=user_data["email"], password=user_data["password"])
        db.add(user)
        db.commit()

        student = Student(user=user)
        db.add(student)
        db.commit()
        assert student.id is not None
        assert student.user_id == user.id

    def test_student_uniqueness(self, db: Session, user_data: dict):
        user = User(name=user_data["name"], email=user_data["email"], password=user_data["password"])
        db.add(user)
        db.commit()

        with pytest.raises(IntegrityError):
            student1 = Student(user=user)
            student2 = Student(user=user)
            db.add_all([student1, student2])
            db.commit()
