import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.schemas.login_schema import LoginData
from src.schemas.user_schema import UserCreate
from src.services.auth_service import AuthService
from src.services.user_service import UserService


class TestClass:
    def test_login_for_access_token_success(self, db: Session, user_data: LoginData):
        auth_service = AuthService(db)
        user_service = UserService(db)
        user = user_service.create_user(UserCreate(**user_data))
        result = auth_service.login_for_access_token(LoginData(**user_data))

        assert result.user.email == user.email
        assert result.user.name == user.name

    def test_login_for_access_token_failure_when_user_do_not_exist(self, db, user_data):
        auth_service = AuthService(db)
        with pytest.raises(HTTPException):
            auth_service.login_for_access_token(LoginData(**user_data))

    def test_login_for_access_token_failure_when_password_is_not_valid(self, db, user_data):
        auth_service = AuthService(db)
        user_service = UserService(db)
        user_service.create_user(UserCreate(**user_data))

        user_data["password"] = "123"
        with pytest.raises(HTTPException):
            auth_service.login_for_access_token(LoginData(**user_data))
