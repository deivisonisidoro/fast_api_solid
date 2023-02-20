from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.orm import Session

from src.schemas.user_schema import UserCreate, UserOut, UserUpdate


class IUserController(ABC):
    @abstractmethod
    def create_user(self, user: UserCreate, db: Session) -> UserOut:
        pass

    @abstractmethod
    def get_user(self, user_id: int, db: Session) -> UserOut:
        pass

    @abstractmethod
    def list_users(self, db: Session) -> List[UserOut]:
        pass

    @abstractmethod
    def update_user(self, user_id: int, user_update: UserUpdate, db: Session) -> UserOut:
        pass

    @abstractmethod
    def delete_user(self, user_id: int, db: Session):
        pass
