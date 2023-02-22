from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from src.schemas.login_schema import LoginData
from src.schemas.user_schema import UserIn


class IAuthController(ABC):
    @abstractmethod
    def login(self, login_data: LoginData, db: Session) -> dict:
        pass

    @abstractmethod
    def get_profile(user: UserIn):
        pass
