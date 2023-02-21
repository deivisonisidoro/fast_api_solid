from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.user_models import User
from src.providers.password_manager import PasswordManager
from src.schemas.user_schema import UserCreate, UserUpdate

from .interfaces.iuser_repository import IUserRepository


class UserRepository(IUserRepository):
    def __init__(
        self,
        db: Session,
        password_manager: Optional[PasswordManager] = None,
    ):
        self.db = db
        self.password_manager = password_manager if password_manager else PasswordManager()

    def create_user(self, user: UserCreate) -> User:
        user.password = self.password_manager.hash_generate(user.password)
        db_user = User(name=user.name, email=user.email, password=user.password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def get_all_users(self) -> List[User]:
        return self.db.query(User).all()

    def update_user(self, user: User, user_update: UserUpdate) -> User:
        user.name = user_update.name or user.name
        user.email = user_update.email or user.email

        if user_update.password:
            user.password = self.password_manager.hash_generate(user_update.password)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user_password(self, user: User, password: str) -> User:
        user.password = self.password_manager.hash_generate(password)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user: User):
        self.db.delete(user)
        self.db.commit()
