from dataclasses import dataclass

from fastapi import BackgroundTasks, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from fastapi_mail import MessageType
from sqlalchemy.orm import Session

from src.providers.email_provider import EmailProvider
from src.providers.interfaces.iemail_provider import IEmailProvider
from src.providers.interfaces.itoken_manager import ITokenManagerProvider
from src.providers.token_manager_provider import TokenManagerProvider
from src.repositories.interfaces.iuser_repository import IUserRepository
from src.repositories.user_repository import UserRepository
from src.schemas.user_schema import PasswordReset, UserCreate, UserUpdate


@dataclass
class UserService:
    db: Session
    token_manager: ITokenManagerProvider = TokenManagerProvider()
    email_provider: IEmailProvider = EmailProvider()
    templates: Jinja2Templates = Jinja2Templates(directory="src/templates")

    def __post_init__(self):
        self._user_repository: IUserRepository = UserRepository(self.db)

    def create_user(self, user: UserCreate):
        db_user = self._user_repository.get_user_by_email(user.email)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        user_created = self._user_repository.create_user(user)
        return user_created

    def get_user(self, user_id: int):
        user = self._user_repository.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user

    def list_users(self):
        return self._user_repository.get_all_users()

    def update_user(self, user_id: int, user_update: UserUpdate):
        db_user = self._user_repository.get_user_by_id(user_id)

        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return self._user_repository.update_user(db_user, user_update)

    def delete_user(self, user_id: int):
        db_user = self._user_repository.get_user_by_id(user_id)

        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return self._user_repository.delete_user(db_user)

    async def reset_password_request(self, email: str, request: Request, background_tasks: BackgroundTasks) -> dict:
        user = self._user_repository.get_user_by_email(email)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        jwt_token = self.token_manager.generate_jwt_token(user_email=user.email)
        html = self.templates.TemplateResponse(
            "password_reset_request.html",
            {"request": request, "jwt_token": jwt_token, "user_name": user.name},
        ).body
        await self.email_provider.send_email(
            recipients=[user.email],
            subject="Reset Password",
            body=html,
            subtype=MessageType.html,
            background_tasks=background_tasks,
        )
        return {"detail": "Password reset link sent successfully"}

    def reset_password(self, password_reset: PasswordReset):
        decoded_token = self.token_manager.decode_jwt_token(password_reset.token)
        user = self._user_repository.get_user_by_email(decoded_token["email"])

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        self._user_repository.update_user_password(user, password_reset.password)
        return {"access_token": self.token_manager.generate_jwt_token(user.email)}
