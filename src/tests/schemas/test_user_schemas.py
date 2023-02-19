from datetime import datetime

import pytest
from pydantic import ValidationError

from src.schemas.user_schema import *


class TestUserSchemas:
    @pytest.fixture
    def user_in(self):
        return UserIn(name="John Doe", email="johndoe@example.com", password="secret")

    @pytest.fixture
    def user_db(self):
        return UserDB(
            id=1, name="John Doe", email="johndoe@example.com", password="hashed_secret", created_at=datetime.now()
        )

    def test_user_in(self, user_in):
        assert user_in.name == "John Doe"
        assert user_in.email == "johndoe@example.com"
        assert user_in.password == "secret"

    def test_user_out(self, user_db):
        user_out = UserOut.from_orm(user_db)
        assert user_out.id == 1
        assert user_out.name == "John Doe"
        assert user_out.email == "johndoe@example.com"
        assert user_out.created_at == user_db.created_at

    def test_user_create(self):
        user_create = UserCreate(name="John Doe", email="johndoe@example.com", password="secret")
        assert user_create.name == "John Doe"
        assert user_create.email == "johndoe@example.com"
        assert user_create.password == "secret"

        with pytest.raises(ValidationError):
            UserCreate(name="John Doe", email="johndoeexample.com", password="secret")

    def test_user_update(self):
        user_update = UserUpdate(name="Jane Doe", email="janedoe@example.com")
        assert user_update.name == "Jane Doe"
        assert user_update.email == "janedoe@example.com"
        assert user_update.password is None
