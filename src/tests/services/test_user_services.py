import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.providers.password_manager_provider import PasswordManagerProvider
from src.schemas.user_schema import PasswordReset, UserCreate, UserUpdate
from src.services.user_service import UserService


class TestUserService:
    """
    Class to test UserService methods.
    """

    def test_create_user(self, db: Session, user_data: UserCreate):
        """
        Test case to create a user.

        Args:
            db (Session): SQLAlchemy database session.
            user_data (UserCreate): UserCreate schema object.

        Expected Result:
            The created user should have a non-null id and its attributes should match the input user_data.

        Steps:
            1. Create a UserService object.
            2. Call the create_user method with the input user_data.
            3. Assert that the created user has a non-null id and its attributes match the input user_data.
        """
        result = UserService(db).create_user(UserCreate(**user_data))
        assert result.id is not None
        assert result.name == user_data["name"]
        assert result.email == user_data["email"]

    def test_get_user(self, db: Session, user_data: UserCreate):
        """
        Test case to get a user by id.

        Args:
            db (Session): SQLAlchemy database session.
            user_data (UserCreate): UserCreate schema object.

        Expected Result:
            The returned user should have attributes that match the created user.

        Steps:
            1. Create a UserService object.
            2. Create a user using the input user_data.
            3. Call the get_user method with the id of the created user.
            4. Assert that the returned user has attributes that match the created user.
        """
        service = UserService(db)
        result = service.create_user(UserCreate(**user_data))
        get_result = service.get_user(result.id)
        assert get_result.id == result.id
        assert get_result.name == result.name
        assert get_result.email == result.email

    def test_list_users(self, db: Session, user_data: UserCreate):
        """
        Test case to list all users.

        Args:
            db (Session): SQLAlchemy database session.
            user_data (UserCreate): UserCreate schema object.

        Expected Result:
            The returned list should contain all the created users.

        Steps:
            1. Create a UserService object.
            2. Create two users using the input user_data and different email and password.
            3. Call the list_users method.
            4. Assert that the returned list contains all the created users.
        """
        service = UserService(db)
        user1 = UserCreate(**user_data)
        user2 = UserCreate(name="Test User 2", email="test2@example.com", password="password")
        service.create_user(user1)
        service.create_user(user2)
        result = service.list_users()
        assert len(result) == 2

    def test_update_user(self, db: Session, user_data: UserCreate):
        """
        Test updating a user's information.

        Args:
            db (Session): The SQLAlchemy session object.
            user_data (UserCreate): The user data to use for creating the user.

        Steps:
            1. Create a user with the given user data.
            2. Call the `update_user` method of the `UserService` with the user ID and the new user information.
            3. Assert that the returned user object has the same ID as the original user.
            4. Assert that the returned user object has the updated name and email.
            5. Assert that the returned user object's password is the same as the original user.

        Expected Results:
            The user object returned by the `update_user` method should have the same ID as the original user,
            an updated name and email, and the same password as the original user.
        """
        service = UserService(db)
        result = service.create_user(UserCreate(**user_data))
        assert result.id is not None
        assert result.name == user_data["name"]
        assert result.email == user_data["email"]
        update_user = UserUpdate(name="Update User", email="test@example.com", password="password")
        updated_result = service.update_user(result.id, update_user)
        assert updated_result.id == result.id
        assert updated_result.name == update_user.name
        assert updated_result.email == result.email

    def test_delete_user(self, db: Session, user_data: UserCreate):
        """
        Test deleting a user.

        Args:
            db (Session): The SQLAlchemy session object.
            user_data (UserCreate): The user data to use for creating the user.
        Steps:
            1. Create a user with the given user data.
            2. Call the `delete_user` method of the `UserService` with the user ID.
            3. Assert that calling the `get_user` method of the `UserService` with the same user ID raises an HTTPException.

        Expected Results:
            Calling the `get_user` method of the `UserService` with the user ID after calling the `delete_user` method
            should raise an HTTPException.
        """
        service = UserService(db)
        result = service.create_user(UserCreate(**user_data))
        assert result.id is not None
        assert result.name == user_data["name"]
        assert result.email == user_data["email"]

        # delete the user and ensure it cannot be retrieved
        service.delete_user(result.id)
        with pytest.raises(HTTPException):
            service.get_user(result.id)

    def test_reset_password(self, db: Session, user_data: UserCreate, mocker):
        """
        Test resetting a user's password.

        Steps:
        1. Create a user with the given user data.
        2. Generate a JWT token for the user's email address.
        3. Create a `PasswordReset` object with the token, a new password, and the user's email address.
        4. Mock the `hash_password` method of the `UserService` to return a fixed hash value.
        5. Call the `reset_password` method of the `UserService` with the `PasswordReset` object.
        6. Assert that the returned dictionary has an "access_token" key with a non-null value.
        7. Retrieve the user with the `get_user` method of the `UserService`.
        8. Assert that the user's password has been updated to the new password.

        Args:
            db (Session): The SQLAlchemy session.
            user_data (UserCreate): The user data to create the user with.
            mocker: The pytest mocker object.

        Expected Results:
            The user's password should be updated to the new password.

        Explanation:
            This test function tests the `reset_password` method of the `UserService`. It creates a user with the given user
            data, generates a JWT token for the user's email address, and creates a `PasswordReset` object with the token, a new
            password, and the user's email address. It then mocks the `hash_password` method of the `UserService` to return a
            fixed hash value, calls the `reset_password` method of the `UserService` with the `PasswordReset` object, and asserts
            that the returned dictionary has an "access_token" key with a non-null value. Finally, it retrieves the user with
            the `get_user` method of the `UserService` and asserts that the user's password has been updated to the new password.
        """
        service = UserService(db)

        # Create a user with the given user data
        user = service.create_user(UserCreate(**user_data))

        # Generate a JWT token for the user's email address
        token = service.token_manager.generate_jwt_token(user.email)

        # Create a `PasswordReset` object with the token, a new password, and the user's email address
        password_reset = PasswordReset(token=token, password="newpassword", email=user.email)

        # Mock the `hash_password` method of the `UserService` to return a fixed hash value
        service.hash_password = mocker.Mock(return_value="hashedpassword")

        # Call the `reset_password` method of the `UserService` with the `PasswordReset` object
        result = service.reset_password(password_reset)

        # Assert that the returned dictionary has an "access_token" key with a non-null value
        assert "access_token" in result
        assert result["access_token"] is not None

        # Retrieve the user with the `get_user` method of the `UserService`
        updated_user = service.get_user(user.id)

        # Assert that the user's password has been updated to the new password
        assert PasswordManagerProvider().hash_verify(password_reset.password, updated_user.password) is True
