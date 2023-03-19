from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.config.database import Base


class Administrator(Base):
    """
    Represents an administrator in the database.

    This SQLAlchemy model maps to the 'administrator' table in the database, and defines the columns and constraints for
    storing administrator information.

    Attributes:
        id (int): The primary key of the administrator table.
        user_id (int): The foreign key to the corresponding user of the administrator, with a unique constraint.
        user (User): The user object of the corresponding user of the administrator.
        created_at (datetime): The timestamp for when the administrator was created.
        updated_at (datetime): The timestamp for when the administrator was last updated.

    Table name:
        administrator: The name of the table in the database that this SQLAlchemy model maps to.

    Columns:
        id: The primary key column for the administrator table.
        user_id: The foreign key column to the users table.
        created_at: The timestamp column for when the administrator was created.
        updated_at: The timestamp column for when the administrator was last updated.

    Table arguments:
        uq_administrator_user_id (UniqueConstraint): A unique constraint on the user_id column that ensures no two administrators share
        the same user.

    """

    __tablename__ = "administrator"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    user = relationship("User", backref="admins")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
