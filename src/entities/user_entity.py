from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint
from sqlalchemy.sql import func

from src.config.database import Base


class User(Base):
    """
    Defines a SQLAlchemy model for the 'users' table in the database.

    Attributes:
        id (int): Primary key column for the user.
        name (str): Name of the user. Maximum length is 50 characters.
        email (str): Email address of the user. Must be unique and maximum length is 255 characters.
        password (str): Password for the user.
        created_at (datetime): Timestamp for when the user was created.
        updated_at (datetime): Timestamp for when the user was last updated.

    Constraints:
        uq_users_email (UniqueConstraint): Unique constraint for the email column.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True, nullable=False, info={"max_length": 50})
    email = Column(String(255), unique=True, index=True, nullable=False, info={"max_length": 255})
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (UniqueConstraint("email", name="uq_users_email"),)
