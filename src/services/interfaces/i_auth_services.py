from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session

from src.schemas.login_schema import LoginData, SuccessLogin


@dataclass
class IAuthService(ABC):
    """Abstract base class for authentication services.

    Args:
        db: SQLAlchemy Session instance

    Attributes:
        db (Session): SQLAlchemy Session instance
    """

    db: Session

    @abstractmethod
    def login_for_access_token(self, login_data: LoginData) -> SuccessLogin:
        """Validate user login credentials and return an access token.

        Args:
            login_data: LoginData schema containing user login credentials

        Returns:
            SuccessLogin schema containing user information and access token
        """
        pass
