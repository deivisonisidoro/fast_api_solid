from abc import ABC, abstractmethod
from typing import Any, List

from fastapi import BackgroundTasks, Request

from src.schemas.token_schema import TokenOut
from src.schemas.user_schema import PasswordReset, UserCreate, UserOut, UserUpdate
from src.services.interfaces.i_user_services import IUserService


class IUserRouters(ABC):
    @abstractmethod
    def create_user(self, user: UserCreate, user_service: IUserService) -> UserOut:
        pass

    @abstractmethod
    def get_user(self, user_id: int, user_service: IUserService) -> UserOut:
        pass

    @abstractmethod
    def list_users(self, user_service: IUserService) -> List[UserOut]:
        pass

    @abstractmethod
    def update_user(self, user_id: int, user_update: UserUpdate, user_service: IUserService) -> UserOut:
        pass

    @abstractmethod
    def delete_user(self, user_id: int, user_service: IUserService) -> Any:
        pass

    @abstractmethod
    def reset_password_request(
        self, email: str, request: Request, background_tasks: BackgroundTasks, user_service: IUserService
    ):
        pass

    @abstractmethod
    def password_reset(password_reset: PasswordReset, user_service: IUserService) -> TokenOut:
        pass
