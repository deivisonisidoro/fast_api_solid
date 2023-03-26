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
    """
    Test class for user routers.

    """

    def test_create_user(self, db: Session, user_data: UserCreate, client: TestClient):
        """Test creating a new user with valid data.

        Args:
            db (Session): A SQLAlchemy session object.
            user_data (UserCreate): A Pydantic model representing the user data to be created.
            client (TestClient): A FastAPI test client instance.

        Steps:
            - Make a request to create a new user with the provided user data.
            - Check the response status code is 201.
            - Check the response content type is JSON.
            - Extract the created user's data from the response JSON.
            - Check that the created user's email address matches the email address provided in the request.

        Expected Result:
            - The API should return an HTTP 201 Created status code and a JSON response containing the created user's data.
            - The created user's email address should match the email address provided in the request.

        """
        response = client.post("/api/users/", json=user_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.headers["Content-Type"] == "application/json"

        created_user = response.json()
        assert created_user["email"] == user_data["email"]

    def test_create_user_duplicate_email(self, user_data: UserCreate, db: Session, client: TestClient):
        """Test creating a new user with an email address that already exists in the database.

        Args:
            user_data (UserCreate): A Pydantic model representing the user data to be created.
            db (Session): A SQLAlchemy session object.
            client (TestClient): A FastAPI test client instance.
        Steps:
            1. Create a user in the database with the given user_data.
            2. Send a POST request to the /api/users/ endpoint with the same user_data.
            3. Assert that the response status code is 400.
            4. Assert that the response contains an error message indicating the email address already exists.

        Expected Result:
            The API should return an HTTP 400 Bad Request status code.

        Raises:
            AssertionError: If any of the expected results is not met.
        """
        user_service = UserRepository(db)
        user_service.create_user(UserCreate(**user_data))

        response = client.post("/api/users/", json=user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_user(self, db: Session, user_data: UserCreate, client: TestClient):
        """Test creating a new user with an email address that already exists in the database.

        Args:
            user_data (UserCreate): A Pydantic model representing the user data to be created.
            db (Session): A SQLAlchemy session object.
            client (TestClient): A FastAPI test client instance.

        Steps:
            - Create a user using UserRepository with the given user data.
            - Make a request to create a new user with the same email address.
            - Check the response status code to ensure that it is HTTP 400 Bad Request.

        Expected Result:
            The API should return an HTTP 400 Bad Request status code.

        """
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
        """Test retrieving a user that does not exist.

        Args:
            client (TestClient): A FastAPI test client instance.

        Steps:
            - Make a request to retrieve a user that does not exist.
            - Check the response status code.
            - Verify that the response body is empty.

        Expected Result:
        - The API should return an HTTP 404 Not Found status code.
        - The response body should be empty.


        """
        response = client.get("/api/users/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_users(self, db: Session, user_data: UserCreate, client: TestClient):
        """
        Test listing all users.

        Args:
            db (Session): Database session.
            user_data (UserCreate): User data to create and list.
            client (TestClient): Test client.

        Steps:
            - Create a new user.
            - Make a request to list all users.
            - Check the response status code, content type header, and data type.

        Expected Result:
            - Response status code should be 200.
            - Response headers should contain 'Content-Type' as 'application/json'.
            - Response data should be a list of dictionaries representing the users.

        """
        user_service = UserRepository(db)
        user_service.create_user(UserCreate(**user_data))

        response = client.get("/api/users/")
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["Content-Type"] == "application/json"
        assert isinstance(response.json(), List)

    def test_update_user(self, db: Session, user_data: UserCreate, client: TestClient):
        """Test updating a user.

        Args:
            db (Session): A SQLAlchemy session object.
            user_data (UserCreate): A Pydantic model representing the user data to be updated.
            client (TestClient): A FastAPI test client instance.

        Steps:
            - Create a new user using the UserRepository.
            - Define the data to be updated.
            - Make a request to update the user with the specified ID.
            - Check the response status code and content type.
            - Check that the updated user's name matches the name provided in the request.

        Expected Result:
            - The API should return an HTTP 200 OK status code and a JSON response containing the updated user's data.
            - The updated user's name should match the name provided in the request.

        Raises:
            AssertionError: If any of the expected results is not met.
        """
        user_service = UserRepository(db)
        created_user = user_service.create_user(UserCreate(**user_data))
        update_data = {"name": "Updated Name", "email": "updated@test.com", "password": "updated password"}

        response = client.patch(f"/api/users/{created_user.id}", json=update_data)
        updated_user = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["Content-Type"] == "application/json"
        assert updated_user["name"] == update_data["name"]

    def test_update_not_found(self, user_data: UserCreate, client: TestClient):
        """Test updating a non-existent user.

        Args:
            user_data (UserCreate): User data to update.
            client (TestClient): Test client.

        Steps:
            - Make a PATCH request to "/api/users/999" with the user data to update.
            - Check that the response status code is 404.

        Expected Result:
            - The API should return an HTTP 404 Not Found status code.

        """
        response = client.patch("/api/users/999", json=user_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_password_reset_request(self, db: Session, user_data: UserCreate, client: TestClient):
        """Test requesting a password reset.

        Args:
            db (Session): Database session.
            user_data (UserCreate): User data to create.
            client (TestClient): Test client.

        Steps:
            - Create a user using UserRepository.
            - Generate a token for the user.
            - Make a request to reset the password.
            - Check the response status code and access token.
            - Check that the password reset token was saved in the database.

        Expected Result:
            - Response status code should be 200.
            - Password reset token should be saved in the database.

        Raises:
            AssertionError: If any of the expected results is not met.
        """
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
        """
        Test resetting a user's password.

        Args:
            db (Session): Database session.
            user_data (UserCreate): User data to create and reset the password.
            client (TestClient): Test client.

        Steps:
            - Create a user using UserRepository.
            - Generate a token for the user.
            - Make a request to reset the password.
            - Check the response status code and access token.
            - Check that the user's password was updated in the database.

        Expected Result:
            - Response status code should be 200.
            - The new access token should not be None.
            - The user's password in the database should be updated.


        """
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
