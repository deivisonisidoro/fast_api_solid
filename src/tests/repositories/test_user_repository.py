from sqlalchemy.orm import Session

from src.repositories.user_repository import UserRepository
from src.schemas.user_schema import UserCreate, UserUpdate


class TestUserRepository:
    def test_create_user(self, db: Session, user_data: dict):
        """
        Test creating a user in the database.

        Args:
            db (Session): SQLAlchemy database session object.
            user_data (dict): Dictionary containing user data.

        Expected Results:
            The method should create a user in the database with the provided data.
            The method should return the created user object with the generated ID.
            The created user object should have the same name and email as the provided user data.
            The password of the created user object should be hashed and not equal to the provided password.
        """
        user_repo = UserRepository(db)
        user = user_repo.create_user(UserCreate(**user_data))
        assert user.id is not None
        assert user.name == user_data["name"]
        assert user.email == user_data["email"]
        assert user.password != user_data["password"]

    def test_get_user_by_id(self, db: Session, user_data: dict):
        """
        Test retrieving a user by ID from the database.

        Args:
            db (Session): SQLAlchemy database session object.
            user_data (dict): Dictionary containing user data.

        Expected Results:
            The method should retrieve the created user object by ID from the database.
            The retrieved user object should have the same name, email, and password as the created user object.
        """
        user_repo = UserRepository(db)
        user = user_repo.create_user(UserCreate(**user_data))
        retrieved_user = user_repo.get_user_by_id(user.id)
        assert retrieved_user is not None
        assert retrieved_user.id == user.id
        assert retrieved_user.name == user.name
        assert retrieved_user.email == user.email
        assert retrieved_user.password == user.password

    def test_get_user_by_email(self, db: Session, user_data: dict):
        """
        Test retrieving a user by email from the database.

        Args:
            db (Session): SQLAlchemy database session object.
            user_data (dict): Dictionary containing user data.

        Expected Results:
            The method should retrieve the created user object by email from the database.
            The retrieved user object should have the same name, email, and password as the created user object.
        """
        user_repo = UserRepository(db)
        user = user_repo.create_user(UserCreate(**user_data))
        retrieved_user = user_repo.get_user_by_email(user.email)
        assert retrieved_user is not None
        assert retrieved_user.id == user.id
        assert retrieved_user.name == user.name
        assert retrieved_user.email == user.email
        assert retrieved_user.password == user.password

    def test_get_all_users(self, db: Session, user_data: dict):
        """
        Test retrieving all users from the database.

        Args:
            db (Session): SQLAlchemy database session object.
            user_data (dict): Dictionary containing user data.

        Expected Results:
            The method should retrieve all created user objects from the database.
            The method should return a list of user objects.
            The length of the list should be equal to the number of created users.
        """
        user_data_2 = {"name": "Jane Doe", "email": "janedoe@example.com", "password": "password456"}
        user_repo = UserRepository(db)
        user_repo.create_user(UserCreate(**user_data))
        user_repo.create_user(UserCreate(**user_data_2))
        all_users = user_repo.get_all_users()
        assert len(all_users) == 2

    def test_update_user(self, db: Session, user_data: dict):
        """
        Test updating an existing user in the database.

        Args:
            db (Session): SQLAlchemy database session object
            user_data (dict): Dictionary containing user data

        Expected Results:
            The updated user should have the same ID as the original user, and its
            name and email should be updated to the values in the updated_user_data
            dictionary. The updated user's password should not be equal to the
            password in updated_user_data.
        """
        user_repo = UserRepository(db)
        user = user_repo.create_user(UserCreate(**user_data))
        updated_user_data = {"name": "Jane Doe", "email": "janedoe@example.com", "password": "newpassword789"}
        updated_user = user_repo.update_user(user, UserUpdate(**updated_user_data))
        assert updated_user.id == user.id
        assert updated_user.name == updated_user_data["name"]
        assert updated_user.email == updated_user_data["email"]
        assert updated_user.password != updated_user_data["password"]

    def test_delete_user(self, db: Session, user_data: dict):
        """
        Test deleting an existing user from the database.

        Args:
            db (Session): SQLAlchemy database session object
            user_data (dict): Dictionary containing user data

        Expected Results:
            After deleting a user from the database, the get_user_by_id method
            should return None when called with the deleted user's ID.
        """
        user_repo = UserRepository(db)
        user = user_repo.create_user(UserCreate(**user_data))
        user_repo.delete_user(user)
        assert user_repo.get_user_by_id(user.id) is None
