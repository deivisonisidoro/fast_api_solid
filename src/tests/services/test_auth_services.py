import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.schemas.login_schema import LoginData
from src.schemas.user_schema import UserCreate
from src.services.auth_service import AuthService
from src.services.user_service import UserService


class TestAuthServices:
    """
    Test suite for testing the AuthService login_for_access_token method.

    Methods:
        - test_login_for_access_token_success:
            Test that a user can successfully login and retrieve an access token.
        - test_login_for_access_token_failure_when_user_do_not_exist:
            Test that an HTTPException is raised when the user does not exist.
        - test_login_for_access_token_failure_when_password_is_not_valid:
            Test that an HTTPException is raised when the password is not valid.
    """

    def test_login_for_access_token_success(self, db: Session, user_data: LoginData):
        """
        Test that a user can successfully login and retrieve an access token.

        Args:
            db (Session): SQLAlchemy session object
            user_data (LoginData): Data required to login (username and password)

        Steps:
            1. Create an instance of AuthService and UserService with the db parameter
            2. Use the UserService instance to create a new user with the given user_data
            3. Call the AuthService login_for_access_token method with the user_data
            4. Check that the returned user's email and name match the created user's email and name.

        Expected Results:
            The test will pass if the access token is successfully generated and the
            returned user's email and name match the user that was created.
        """
        auth_service = AuthService(db)
        user_service = UserService(db)
        user = user_service.create_user(UserCreate(**user_data))
        result = auth_service.login_for_access_token(LoginData(**user_data))

        assert result.user.email == user.email
        assert result.user.name == user.name

    def test_login_for_access_token_failure_when_user_do_not_exist(self, db, user_data):
        """
        Test that an HTTPException is raised when the user does not exist.

        Args:
            db (Session): SQLAlchemy session object
            user_data (LoginData): Data required to login (username and password)

        Steps:
            1. Create an instance of AuthService with the db parameter
            2. Use a pytest.raises context manager to check that an HTTPException is raised
               when calling the AuthService login_for_access_token method with user_data.

        Expected Results:
            The test will pass if an HTTPException is raised when trying to login with
            non-existent user_data.
        """
        auth_service = AuthService(db)
        with pytest.raises(HTTPException):
            auth_service.login_for_access_token(LoginData(**user_data))

    def test_login_for_access_token_failure_when_password_is_not_valid(self, db, user_data):
        """
        Test that an HTTPException is raised when the password is not valid.

        Args:
            db (Session): SQLAlchemy session object
            user_data (LoginData): Data required to login (username and password)

        Steps:
            1. Create an instance of AuthService and UserService with the db parameter
            2. Use the UserService instance to create a new user with the given user_data
            3. Change the password of the user_data to an invalid password
            4. Use a pytest.raises context manager to check that an HTTPException is raised
               when calling the AuthService login_for_access_token method with the modified user_data.

        Expected Results:
            The test will pass if an HTTPException is raised when trying to login with
            invalid password.

        """
        auth_service = AuthService(db)
        user_service = UserService(db)
        user_service.create_user(UserCreate(**user_data))

        user_data["password"] = "123"
        with pytest.raises(HTTPException):
            auth_service.login_for_access_token(LoginData(**user_data))
