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
    @patch.object(TokenManagerProvider, "create_access_token")
    def test_login_for_access_token_success(
        self,
        mock_create_access_token,
        db: Session,
        client: TestClient,
        user_data: dict,
    ):
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
        user_service = UserRepository(db)
        user_service.create_user(UserCreate(**user_data))

        response = client.get("/api/auth/profile", headers={"Authorization": f"Bearer 1234"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.headers["Content-Type"] == "application/json"
        assert response.json() == {"detail": "Token is not authorized"}
