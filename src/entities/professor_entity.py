from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.config.database import Base


class Professor(Base):
    """
    Represents a professor in the database.

    This SQLAlchemy model maps to the 'professors' table in the database, and defines the columns and constraints for
    storing professor information.

    Attributes:
        id (int): The primary key of the professor table.
        user_id (int): The foreign key referencing the corresponding user of this professor.
        user (User): The corresponding user of this professor.
        created_at (datetime): The timestamp for when the professor was created.
        updated_at (datetime): The timestamp for when the professor was last updated.

    Table name:
        professors: The name of the table in the database that this SQLAlchemy model maps to.

    Columns:
        id: The primary key column for the professor table.
        user_id: The foreign key column referencing the user table.
        created_at: The timestamp column for when the professor was created.
        updated_at: The timestamp column for when the professor was last updated.

    Table arguments:
        None

    """

    __tablename__ = "professors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    user = relationship("User", backref="professors")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
