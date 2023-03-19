from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint
from sqlalchemy.sql import func

from src.config.database import Base


class User(Base):
    """
    Represents a user in the database.

    This SQLAlchemy model maps to the 'users' table in the database, and defines the columns and constraints for
    storing user information.

    Attributes:
        id (int): The primary key of the user table.
        name (str): The name of the user, with a maximum length of 50 characters.
        email (str): The email address of the user, with a maximum length of 255 characters. Must be unique.
        password (str): The user's password.
        created_at (datetime): The timestamp for when the user was created.
        updated_at (datetime): The timestamp for when the user was last updated.

    Constraints:
        uq_users_email (UniqueConstraint): A unique constraint that ensures no two users share the same email.

    Table name:
        users: The name of the table in the database that this SQLAlchemy model maps to.

    Columns:
        id: The primary key column for the user table.
        name: The name column for the user table.
        email: The email column for the user table.
        password: The password column for the user table.
        created_at: The timestamp column for when the user was created.
        updated_at: The timestamp column for when the user was last updated.

    Table arguments:
        uq_users_email (UniqueConstraint): A unique constraint on the email column that ensures no two users share
        the same email.

    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True, nullable=False, info={"max_length": 50})
    email = Column(String(255), unique=True, index=True, nullable=False, info={"max_length": 255})
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (UniqueConstraint("email", name="uq_users_email"),)
