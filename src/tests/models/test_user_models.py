import pytest
from sqlalchemy.exc import IntegrityError

from src.models import User


class TestUserModel:
    def test_create_user(self, db):
        # test
        user = User(name="Test User", email="test@example.com", password="password")
        db.add(user)
        db.commit()

        # assert
        assert user.id is not None
        assert user.name == "Test User"
        assert user.email == "test@example.com"
        assert user.password == "password"

        # cleanup
        db.rollback()

    def test_create_duplicate_user(self, db):
        # create a user
        user = User(name="Test User", email="testuser@example.com", password="password")
        db.add(user)
        db.commit()

        # attempt to create a user with the same email
        with pytest.raises(IntegrityError):
            user2 = User(name="Test User 2", email="testuser@example.com", password="password")
            db.add(user2)
            db.commit()
