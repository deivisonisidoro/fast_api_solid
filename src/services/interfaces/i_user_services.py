from abc import ABC, abstractmethod
from typing import List

from fastapi import BackgroundTasks, Request

from src.schemas.user_schema import UserCreate, UserUpdate


class IUserService(ABC):
    @abstractmethod
    def create_user(self, user: UserCreate) -> dict:
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> dict:
        pass

    @abstractmethod
    def list_users(self) -> List[dict]:
        pass

    @abstractmethod
    def update_user(self, user_id: int, user_update: UserUpdate) -> dict:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> dict:
        pass

    @abstractmethod
    async def reset_password_request(self, email: str, request: Request, background_tasks: BackgroundTasks) -> dict:
        pass

    @abstractmethod
    def reset_password(self, token: str, password: str) -> dict:
        pass
