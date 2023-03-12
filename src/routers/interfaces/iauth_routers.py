from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from src.schemas.login_schema import LoginData, SuccessLogin
from src.schemas.user_schema import UserIn


class IAuthRouters(ABC):
    @abstractmethod
    def login_for_access_token(self, login_data: LoginData, db: Session) -> SuccessLogin:
        pass

    @abstractmethod
    def get_profile(user: UserIn):
        pass
