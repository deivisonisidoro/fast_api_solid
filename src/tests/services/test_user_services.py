import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.providers.password_manager_provider import PasswordManagerProvider
from src.schemas.user_schema import PasswordReset, UserCreate, UserUpdate
from src.services.user_service import UserService


class TestUserService:
    def test_create_user(self, db: Session, user_data: UserCreate):
        result = UserService(db).create_user(UserCreate(**user_data))
        assert result.id is not None
        assert result.name == user_data["name"]
        assert result.email == user_data["email"]

    def test_get_user(self, db: Session, user_data: UserCreate):
        service = UserService(db)
        result = service.create_user(UserCreate(**user_data))
        get_result = service.get_user(result.id)
        assert get_result.id == result.id
        assert get_result.name == result.name
        assert get_result.email == result.email

    def test_list_users(self, db: Session, user_data: UserCreate):
        service = UserService(db)
        user1 = UserCreate(**user_data)
        user2 = UserCreate(name="Test User 2", email="test2@example.com", password="password")
        service.create_user(user1)
        service.create_user(user2)
        result = service.list_users()
        assert len(result) == 2

    def test_update_user(self, db: Session, user_data: UserCreate):
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
        service = UserService(db)
        user = service.create_user(UserCreate(**user_data))

        # create a mock token
        token = service.token_manager.generate_jwt_token(user.email)

        # create a mock PasswordReset object
        password_reset = PasswordReset(token=token, password="newpassword", email=user.email)

        # mock the service's `hash_password` method to return a fixed hash value
        service.hash_password = mocker.Mock(return_value="hashedpassword")

        # call the `reset_password` method and assert the results
        result = service.reset_password(password_reset)
        assert "access_token" in result
        assert result["access_token"] is not None

        # retrieve the user and ensure that the password has been updated
        updated_user = service.get_user(user.id)
        assert PasswordManagerProvider().hash_verify(password_reset.password, updated_user.password) is True
