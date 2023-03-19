# User Entity

The User Entity defines a SQLAlchemy model that represents the users table in the database. It consists of several attributes such as id, name, email, password, created_at, and updated_at.

## Attributes

- `id` (int): Primary key column for the user.
- `name` (str): Name of the user. Maximum length is 50 characters.
- `email` (str): Email address of the user. Must be unique and maximum length is 255 characters.
- `password` (str): The password of the user (stored as a hash).
- `created_at` (datetime): The datetime when the user was created.
- `updated_at` (datetime): The datetime when the user was last updated.

The User Entity is an important part of the project as it represents the user's data and provides a structured way of accessing and manipulating user-related data in the application. The code example provided demonstrates how to define a User entity using SQLAlchemy and shows how to define the different attributes that make up the entity.

## Code Example

Here's an example of `User` entity:

```python
from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint
from sqlalchemy.sql import func

from src.config.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True, nullable=False, info={"max_length": 50})
    email = Column(String(255), unique=True, index=True, nullable=False, info={"max_length": 255})
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (UniqueConstraint("email", name="uq_users_email"),)

```
