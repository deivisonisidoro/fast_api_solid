from datetime import datetime

import pytest
from pydantic import ValidationError

from src.schemas.user_schema import *


class TestUserSchemas:
    """
    Test suite for User schemas.

    Attributes:
        user_in (UserIn): Pydantic schema representing a User input.
        user_db (UserDB): Pydantic schema representing a User stored in the database.
    """

    @pytest.fixture
    def user_in(self) -> UserIn:
        """Fixture for UserIn schema."""
        return UserIn(name="John Doe", email="johndoe@example.com", password="secret")

    @pytest.fixture
    def user_db(self) -> UserDB:
        """Fixture for UserDB schema."""
        return UserDB(
            id=1, name="John Doe", email="johndoe@example.com", password="hashed_secret", created_at=datetime.now()
        )

    def test_user_in(self, user_in: UserIn) -> None:
        """
        Test UserIn schema.

        Args:
            user_in (UserIn): Pydantic schema representing a User input.

        Expected Result:
            The schema  should be correctly created.

        Steps:
            - Assert that the 'name', 'email', and 'password' attributes of the 'user_in' object match the expected values.
        """
        assert user_in.name == "John Doe"
        assert user_in.email == "johndoe@example.com"
        assert user_in.password == "secret"

    def test_user_out(self, user_db: UserDB) -> None:
        """
        Test UserOut schema.

        Args:
            user_db (UserDB): Pydantic schema representing a User stored in the database.

        Expected Result:
            The schema should be correctly created.

        Steps:
            - Create a 'user_out' object by calling the 'from_orm' method of the 'UserOut' schema with the 'user_db' object as argument.
            - Assert that the 'id', 'name', 'email', and 'created_at' attributes of the 'user_out' object match the expected values.
        """
        user_out = UserOut.from_orm(user_db)
        assert user_out.id == 1
        assert user_out.name == "John Doe"
        assert user_out.email == "johndoe@example.com"
        assert user_out.created_at == user_db.created_at

    def test_user_create(self) -> None:
        """
        Test UserCreate schema.

        Expected Result:
            The schema should be correctly created.

        Steps:
            - Create a 'user_create' object by instantiating the 'UserCreate' schema with the expected attributes.
            - Assert that the 'name', 'email', and 'password' attributes of the 'user_create' object match the expected values.
            - Use 'pytest.raises' to check that an exception is raised when creating a 'UserCreate' object with an invalid email address.
        """
        user_create = UserCreate(name="John Doe", email="johndoe@example.com", password="secret")
        assert user_create.name == "John Doe"
        assert user_create.email == "johndoe@example.com"
        assert user_create.password == "secret"

        with pytest.raises(ValidationError):
            UserCreate(name="John Doe", email="johndoeexample.com", password="secret")

    def test_user_update(self):
        """
        Test that UserUpdate schema is created correctly.

        Expected Result:
            The attributes of the UserUpdate object should match the input data.

        Steps:
            1. Create a UserUpdate object with name and email.
            2. Assert that the UserUpdate object's attributes match the input data.
        """
        user_update = UserUpdate(name="Jane Doe", email="janedoe@example.com")
        assert user_update.name == "Jane Doe"
        assert user_update.email == "janedoe@example.com"
        assert user_update.password is None
