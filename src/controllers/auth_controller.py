from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.providers.password_manager import PasswordManager
from src.providers.token_manager import TokenManager
from src.repositories.user_repository import UserRepository
from src.schemas.login_schema import LoginData, SuccessLogin
from src.schemas.user_schema import UserIn, UserOut
from src.utils.auths_utils import get_user_logged_in

from .interfaces.iauth_controller import IAuthController

router = APIRouter()


SECRET_KEY = "key_secret"
ALGORITHM = "HS256"


class AuthController(IAuthController):
    @staticmethod
    @router.post("/token", status_code=status.HTTP_200_OK, response_model=SuccessLogin)
    def login_for_access_token(login_data: LoginData, db: Session = Depends(get_db)) -> dict:
        email = login_data.email
        password = login_data.password
        user_service = UserRepository(db)
        user = user_service.get_user_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or password does not match",
            )
        valid_password = PasswordManager().hash_verify(password, user.password)

        if not valid_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or password does not match",
            )
        access_token = TokenManager().create_access_token({"sub": user.email})
        return SuccessLogin(user=user, access_token=access_token)

    @staticmethod
    @router.get("/profile", status_code=status.HTTP_200_OK, response_model=UserOut)
    async def get_profile(user: UserIn = Depends(get_user_logged_in)):
        return user
