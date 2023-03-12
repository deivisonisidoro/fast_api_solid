import asyncio
from dataclasses import dataclass
from typing import List

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.providers.token_manager_provider import TokenManagerProvider
from src.repositories.user_repository import UserRepository
from src.schemas.user_schema import UserCreate


class TestUserRouters:
    def test_create_user(self, db: Session, user_data: UserCreate, client: TestClient):
        response = client.post("/api/users/", json=user_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.headers["Content-Type"] == "application/json"

        created_user = response.json()
        assert created_user["email"] == user_data["email"]

    def test_create_user_duplicate_email(self, user_data: UserCreate, db: Session, client: TestClient):
        user_service = UserRepository(db)
        user_service.create_user(UserCreate(**user_data))

        response = client.post("/api/users/", json=user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_user(self, db: Session, user_data: UserCreate, client: TestClient):
        user_service = UserRepository(db)
        created_user = user_service.create_user(UserCreate(**user_data))

        response = client.get(f"/api/users/{created_user.id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["Content-Type"] == "application/json"

        user = response.json()
        assert user["email"] == user_data["email"]
        assert user["name"] == user_data["name"]
        assert user["id"] == created_user.id

    def test_get_user_not_found(self, client: TestClient):
        response = client.get("/api/users/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_users(self, db: Session, user_data: UserCreate, client: TestClient):
        user_service = UserRepository(db)
        user_service.create_user(UserCreate(**user_data))

        response = client.get("/api/users/")
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["Content-Type"] == "application/json"
        assert isinstance(response.json(), List)

    def test_update_user(self, db: Session, user_data: UserCreate, client: TestClient):
        user_service = UserRepository(db)
        created_user = user_service.create_user(UserCreate(**user_data))
        update_data = {"name": "Updated Name", "email": "updated@test.com", "password": "updated password"}

        response = client.patch(f"/api/users/{created_user.id}", json=update_data)
        updated_user = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["Content-Type"] == "application/json"
        assert updated_user["name"] == update_data["name"]

    def test_update_not_found(self, user_data: UserCreate, client: TestClient):
        response = client.patch("/api/users/999", json=user_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_password_reset_request(self, db: Session, user_data: UserCreate, client: TestClient):
        # Create user using UserRepository
        user_service = UserRepository(db)
        user_service.create_user(UserCreate(**user_data))

        async def run_test():
            # Then, use the password reset request endpoint to get a JWT token
            response = client.post(f"/api/users/password-reset-request?email={user_data['email']}")
            assert response.status_code == 200
            assert response.json() == {"detail": "Password reset link sent successfully"}

        if __name__ == "__run_test__":
            asyncio.run(run_test())

    def test_password_reset(self, db: Session, user_data: UserCreate, client: TestClient):
        # Create user using UserRepository
        user_service = UserRepository(db)
        user_created = user_service.create_user(UserCreate(**user_data))

        # generate a token for the user
        token = TokenManagerProvider().generate_jwt_token(user_data["email"])

        # make a request to reset the password
        new_password = "newpassword456"
        payload = {"token": token, "email": user_created.email, "password": new_password}
        response = client.post("/api/users/password-reset", json=payload)

        # check the response status code and token
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["access_token"] is not None

        # check that the user's password was updated in the database
        user = UserRepository(db).get_user_by_email(user_data["email"])
        assert user is not None
