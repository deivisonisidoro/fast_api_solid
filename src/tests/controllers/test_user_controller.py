from typing import List

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.repositories.user_repository import UserRepository
from src.schemas.user_schema import UserCreate


class TestUserController:
    def test_create_user(self, db: Session, user_data: dict, client: TestClient):
        response = client.post("/api/users/", json=user_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.headers["Content-Type"] == "application/json"

        created_user = response.json()
        assert created_user["email"] == user_data["email"]

        # Verify that the user was added to the database.
        user_service = UserRepository(db)
        db_user = user_service.get_user_by_email(created_user["email"])
        assert db_user is not None

    def test_create_user_duplicate_email(self, user_data: dict, db: Session, client: TestClient):
        user_service = UserRepository(db)
        user_service.create_user(UserCreate(**user_data))

        response = client.post("/api/users/", json=user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_user(self, db: Session, user_data: dict, client: TestClient):
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

    def test_list_users(self, db: Session, user_data: dict, client: TestClient):
        user_service = UserRepository(db)
        user_service.create_user(UserCreate(**user_data))

        response = client.get("/api/users/")
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["Content-Type"] == "application/json"
        assert isinstance(response.json(), List)

    def test_update_user(self, db: Session, user_data: dict, client: TestClient):
        user_service = UserRepository(db)
        created_user = user_service.create_user(UserCreate(**user_data))
        update_data = {"name": "Updated Name", "email": "updated@test.com", "password": "updated password"}

        response = client.put(f"/api/users/{created_user.id}", json=update_data)
        updated_user = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["Content-Type"] == "application/json"
        assert updated_user["name"] == update_data["name"]

    def test_update_not_found(self, user_data: dict, client: TestClient):
        response = client.put("/api/users/999", json=user_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
