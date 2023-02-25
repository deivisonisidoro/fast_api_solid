from abc import ABC, abstractmethod
from typing import List

from src.entities.user_models import User
from src.schemas.user_schema import UserCreate, UserUpdate


class IUserRepository(ABC):
    @abstractmethod
    def create_user(self, user: UserCreate) -> User:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        pass

    @abstractmethod
    def update_user(self, user: User, user_update: UserUpdate) -> User:
        pass

    @abstractmethod
    def update_user_password(self, user: User, password: str) -> User:
        pass

    @abstractmethod
    def delete_user(self, user: User):
        pass
