from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.entities.administrator_entity import Administrator
from src.entities.user_entity import User


class TestAdministratorEntity:
    def test_create_admin_user(self, db: Session, user_data: dict):
        user = User(name=user_data["name"], email=user_data["email"], password=user_data["password"])
        db.add(user)
        db.commit()

        admin = Administrator(user=user)
        db.add(admin)
        db.commit()
        assert admin.id is not None
        assert admin.user_id == user.id

    def test_administrator_uniqueness(self, db: Session, user_data: dict):
        user = User(name=user_data["name"], email=user_data["email"], password=user_data["password"])
        db.add(user)
        db.commit()

        with pytest.raises(IntegrityError):
            admin1 = Administrator(user=user)
            admin2 = Administrator(user=user)
            db.add_all([admin1, admin2])
            db.commit()
