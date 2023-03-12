import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.entities.professor_entity import Professor
from src.entities.user_entity import User


class TestProfessorEntity:
    def test_create_professor_user(self, db: Session, user_data: dict):
        user = User(name=user_data["name"], email=user_data["email"], password=user_data["password"])
        db.add(user)
        db.commit()

        professor = Professor(user=user)
        db.add(professor)
        db.commit()
        assert professor.id is not None
        assert professor.user_id == user.id

    def test_professor_uniqueness(self, db: Session, user_data: dict):
        user = User(name=user_data["name"], email=user_data["email"], password=user_data["password"])
        db.add(user)
        db.commit()

        with pytest.raises(IntegrityError):
            professor1 = Professor(user=user)
            professor2 = Professor(user=user)
            db.add_all([professor1, professor2])
            db.commit()
