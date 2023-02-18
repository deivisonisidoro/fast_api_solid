from typing import List

from sqlalchemy.orm import Session

from src.models.user_models import User
from src.schemas.user_schema import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate) -> User:
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
        user.password = user_update.password or user.password
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user: User):
        self.db.delete(user)
        self.db.commit()
