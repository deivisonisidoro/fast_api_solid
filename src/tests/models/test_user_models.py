import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.entities import User


class TestUserModel:
    def test_create_user(self, db: Session, user_data: dict):
        # test
        user = User(name=user_data["name"], email=user_data["email"], password=user_data["password"])
        db.add(user)
        db.commit()

        # assert
        assert user.id is not None
        assert user.name == user_data["name"]
        assert user.email == user_data["email"]
        assert user.password == user_data["password"]

        # cleanup
        db.rollback()

    def test_create_duplicate_user(self, db: Session, user_data: dict):
        # create a user
        user = User(name=user_data["name"], email=user_data["email"], password=user_data["password"])
        db.add(user)
        db.commit()

        # attempt to create a user with the same email
        with pytest.raises(IntegrityError):
            user2 = User(name=user_data["name"], email=user_data["email"], password=user_data["password"])
            db.add(user2)
            db.commit()
