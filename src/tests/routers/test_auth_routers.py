from unittest.mock import MagicMock, patch

from fastapi import status
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy.orm import Session

from src.providers.password_manager_provider import PasswordManagerProvider
from src.providers.token_manager_provider import TokenManagerProvider
from src.repositories.user_repository import UserRepository
from src.schemas.user_schema import UserCreate


class TestAuthController:
    """
    Test suite for the AuthController class.
    """

    @patch.object(TokenManagerProvider, "create_access_token")
    def test_login_for_access_token_success(
        self,
        mock_create_access_token,
        db: Session,
        client: TestClient,
        user_data: dict,
    ):
        """
        Test successful user login, which returns an access token.

        Args:
            mock_create_access_token (MagicMock): A mocked version of the create_access_token method from
                TokenManagerProvider.
            db (Session): A SQLAlchemy session.
            client (TestClient): A TestClient instance from FastAPI.
            user_data (dict): A dictionary containing mock user data.

        Expected Results:
            The test should pass if the HTTP response status code is 200 and the response body contains an
            access token.
        """
        mock_create_access_token.return_value = "access_token"
        user_service = UserRepository(db)
        user_service.create_user(UserCreate(**user_data))

        response = client.post("/api/auth/token", json={"email": user_data["email"], "password": user_data["password"]})
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["Content-Type"] == "application/json"

    def test_login_for_access_token_failure(
        self,
        db: Session,
        client: TestClient,
        user_data: dict,
    ):
        """
        Test failed user login, which returns an error message.

        Args:
            db (Session): A SQLAlchemy session.
            client (TestClient): A TestClient instance from FastAPI.
            user_data (dict): A dictionary containing mock user data.

        Expected Results:
            The test should pass if the HTTP response status code is 400 and the response body contains an
            error message.
        """
        user_service = UserRepository(db)
        user_service.create_user(UserCreate(**user_data))

        response = client.post("/api/auth/token", json={"email": user_data["email"], "password": "wrong_password"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.headers["Content-Type"] == "application/json"
        assert response.json() == {"detail": "Email or password does not match"}

    @patch.object(PasswordManagerProvider, "hash_verify")
    def test_get_profile_success(
        self,
        mock_hash_verify,
        db: Session,
        client: TestClient,
        user_data: dict,
    ):
        """
        Test successful retrieval of user profile.

        Args:
            mock_hash_verify (MagicMock): A mocked version of the hash_verify method from PasswordManagerProvider.
            db (Session): A SQLAlchemy session.
            client (TestClient): A TestClient instance from FastAPI.
            user_data (dict): A dictionary containing mock user data.

        Expected Results:
            The test should pass if the HTTP response status code is 200 and the response body contains the user's
            profile data.
        """
        mock_hash_verify.return_value = True
        user_service = UserRepository(db)
        user_service.create_user(UserCreate(**user_data))
        access_token = TokenManagerProvider().create_access_token({"sub": user_data["email"]})

        response = client.get("/api/auth/profile", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["Content-Type"] == "application/json"

    def test_get_profile_failure(
        self,
        db: Session,
        client: TestClient,
        user_data: dict,
    ):
        """
        Test failed retrieval of user profile due to invalid access token.

        Args:
            db (Session): A SQLAlchemy session.
            client (TestClient): A TestClient instance from FastAPI.
            user_data (dict): A dictionary containing mock user data.

        Expected Results:
            The test should pass if the HTTP response status code is 401 and the response body contains an error message
            indicating that the token is not authorized.
        """
        user_service = UserRepository(db)
        user_service.create_user(UserCreate(**user_data))

        response = client.get("/api/auth/profile", headers={"Authorization": f"Bearer 1234"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.headers["Content-Type"] == "application/json"
        assert response.json() == {"detail": "Token is not authorized"}
