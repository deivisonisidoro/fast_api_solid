import os
from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi_mail import MessageType
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.providers.email_provider import EmailProvider
from src.providers.token_manager import TokenManager
from src.repositories.user_repository import UserRepository
from src.schemas.token_schema import TokenOut
from src.schemas.user_schema import PasswordReset, UserCreate, UserOut, UserUpdate

from .interfaces.iuser_controller import IUserController

router = APIRouter()


class UserController(IUserController):
    @staticmethod
    @router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
    async def create_user(user: UserCreate, db: Session = Depends(get_db)):
        user_service = UserRepository(db)
        db_user = user_service.get_user_by_email(user.email)

        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        return user_service.create_user(user)

    @staticmethod
    @router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
    async def get_user(user_id: int, db: Session = Depends(get_db)):
        user_service = UserRepository(db)
        user = user_service.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user

    @staticmethod
    @router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserOut])
    async def list_users(db: Session = Depends(get_db)):
        user_service = UserRepository(db)
        users = user_service.get_all_users()

        return users

    @staticmethod
    @router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
    async def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
        user_service = UserRepository(db)
        db_user = user_service.get_user_by_id(user_id)

        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        updated_user = user_service.update_user(db_user, user_update)
        return updated_user

    @staticmethod
    @router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_user(user_id: int, db: Session = Depends(get_db)):
        user_service = UserRepository(db)
        db_user = user_service.get_user_by_id(user_id)

        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        user_service.delete_user(db_user)
        return {"detail": "User deleted successfully"}

    @staticmethod
    @router.post("/password-reset-request", status_code=status.HTTP_200_OK)
    async def password_reset_request(background_tasks: BackgroundTasks, email: str, db: Session = Depends(get_db)):
        user_service = UserRepository(db)
        user = user_service.get_user_by_email(email)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        jwt_token = TokenManager().generate_jwt_token(user_email=user.email)
        html = f""""<p>Click the following link to reset your password: <a>http://localhost:8000/password-reset?token={jwt_token}<a/></p> """

        email_provider = EmailProvider()
        await email_provider.send_email(
            recipients=[user.email],
            subject="Reset Password",
            body=html,
            subtype=MessageType.html,
            background_tasks=background_tasks,
        )
        return {"detail": "Password reset link sent successfully"}

    @staticmethod
    @router.post("/password-reset", status_code=status.HTTP_200_OK, response_model=TokenOut)
    async def password_reset(password_reset: PasswordReset, db: Session = Depends(get_db)):
        decoded_token = TokenManager().decode_jwt_token(password_reset.token)
        user_service = UserRepository(db)
        user = user_service.get_user_by_email(decoded_token["email"])

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user_service.update_user_password(user, password_reset.password)

        return {"access_token": TokenManager().generate_jwt_token(user.email)}
