from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.providers.token_manager_provider import TokenManagerProvider
from src.repositories.user_repository import UserRepository

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


def verify_token(token: str):
    try:
        email = TokenManagerProvider().verify_access_token(token)
    except JWTError:
        return None
    return email


def get_user_by_email(email: str, db: Session):
    return UserRepository(db).get_user_by_email(email)


def get_user_logged_in(
    token: str = Depends(oauth2_schema),
    db: Session = Depends(get_db),
):
    email = verify_token(token)
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is not authorized")
    user = get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
