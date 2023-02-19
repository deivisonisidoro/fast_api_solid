from sqlalchemy.orm import Session

from src.repositories.user_repository import UserRepository
from src.schemas.user_schema import UserCreate, UserUpdate


class TestUserRepository:
    def test_create_user(self, db: Session, user_data: dict):
        user_repo = UserRepository(db)
        user = user_repo.create_user(UserCreate(**user_data))
        assert user.id is not None
        assert user.name == user_data["name"]
        assert user.email == user_data["email"]
        # assert user.password != user_data["password"]

    def test_get_user_by_id(self, db: Session, user_data: dict):
        user_repo = UserRepository(db)
        user = user_repo.create_user(UserCreate(**user_data))
        retrieved_user = user_repo.get_user_by_id(user.id)
        assert retrieved_user is not None
        assert retrieved_user.id == user.id
        assert retrieved_user.name == user.name
        assert retrieved_user.email == user.email
        # assert retrieved_user.password != user.password

    def test_get_user_by_email(self, db: Session, user_data: dict):
        user_repo = UserRepository(db)
        user = user_repo.create_user(UserCreate(**user_data))
        retrieved_user = user_repo.get_user_by_email(user.email)
        assert retrieved_user is not None
        assert retrieved_user.id == user.id
        assert retrieved_user.name == user.name
        assert retrieved_user.email == user.email

    #     assert retrieved_user.password != user.password

    def test_get_all_users(self, db: Session, user_data: dict):
        user_data_2 = {"name": "Jane Doe", "email": "janedoe@example.com", "password": "password456"}
        user_repo = UserRepository(db)
        user_repo.create_user(UserCreate(**user_data))
        user_repo.create_user(UserCreate(**user_data_2))
        all_users = user_repo.get_all_users()
        assert len(all_users) == 2

    def test_update_user(self, db: Session, user_data: dict):
        user_repo = UserRepository(db)
        user = user_repo.create_user(UserCreate(**user_data))
        updated_user_data = {"name": "Jane Doe", "email": "janedoe@example.com", "password": "newpassword789"}
        updated_user = user_repo.update_user(user, UserUpdate(**updated_user_data))
        assert updated_user.id == user.id
        assert updated_user.name == updated_user_data["name"]
        assert updated_user.email == updated_user_data["email"]

    #     assert updated_user.password != user.password

    def test_delete_user(self, db: Session, user_data: dict):
        user_repo = UserRepository(db)
        user = user_repo.create_user(UserCreate(**user_data))
        user_repo.delete_user(user)
        assert user_repo.get_user_by_id(user.id) is None
