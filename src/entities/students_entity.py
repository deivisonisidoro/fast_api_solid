from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.config.database import Base


class Student(Base):
    """
    Represents a student in the database.

    This SQLAlchemy model maps to the 'students' table in the database, and defines the columns and constraints for
    storing student information.

    Attributes:
        id (int): The primary key of the student table.
        user_id (int): The foreign key of the corresponding user in the 'users' table.
        user (User): The user object associated with this student.
        created_at (datetime): The timestamp for when the student was created.
        updated_at (datetime): The timestamp for when the student was last updated.

    Table name:
        students: The name of the table in the database that this SQLAlchemy model maps to.

    Columns:
        id: The primary key column for the student table.
        user_id: The foreign key column for the corresponding user in the 'users' table.
        created_at: The timestamp column for when the student was created.
        updated_at: The timestamp column for when the student was last updated.

    Table arguments:
        None

    """

    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    user = relationship("User", backref="students")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
