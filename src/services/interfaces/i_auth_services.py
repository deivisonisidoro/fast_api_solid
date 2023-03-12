from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session

from src.schemas.login_schema import LoginData, SuccessLogin


@dataclass
class IAuthService(ABC):
    db: Session

    @abstractmethod
    def login_for_access_token(self, login_data: LoginData) -> SuccessLogin:
        pass
