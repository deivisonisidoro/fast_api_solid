from dataclasses import dataclass

from fastapi import BackgroundTasks, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from fastapi_mail import MessageType
from sqlalchemy.orm import Session

from src.providers.email_provider import EmailProvider
from src.providers.interfaces.iemail_provider import IEmailProvider
from src.providers.interfaces.itoken_manager import ITokenManagerProvider
from src.providers.token_manager_provider import TokenManagerProvider
from src.repositories.interfaces.iuser_repository import IUserRepository
from src.repositories.user_repository import UserRepository
from src.schemas.user_schema import PasswordReset, UserCreate, UserUpdate


@dataclass
class UserService:
    """
    This class acts as the middle layer between the data access layer and the user interface layer. It encapsulates the business logic required for interacting with user data and leverages a repository layer to perform database operations. The class provides a comprehensive set of CRUD (Create, Read, Update, Delete) methods to manage user data effectively.
    Additionally, it includes methods for password reset functionality.

    Args:
        db (Session): The SQLAlchemy session object used for database operations.
        token_manager (ITokenManagerProvider, optional): The token manager provider used for generating and decoding JWT tokens. Defaults to TokenManagerProvider().
        email_provider (IEmailProvider, optional): The email provider used for sending emails. Defaults to EmailProvider().
        templates (Jinja2Templates, optional): The Jinja2Templates object used for rendering email templates. Defaults to Jinja2Templates(directory="src/templates").

    Attributes:
        db (Session): The SQLAlchemy session object used for database operations.
        token_manager (ITokenManagerProvider): The token manager provider used for generating and decoding JWT tokens.
        email_provider (IEmailProvider): The email provider used for sending emails.
        templates (Jinja2Templates): The Jinja2Templates object used for rendering email templates.
    """

    db: Session
    token_manager: ITokenManagerProvider = TokenManagerProvider()
    email_provider: IEmailProvider = EmailProvider()
    templates: Jinja2Templates = Jinja2Templates(directory="src/templates")

    def __post_init__(self):
        """
        Initializes the UserService object after the instance has been created.

        This method initializes the `_user_repository` instance variable with a new instance
        of the `UserRepository` class, passing in the `db` argument that was provided during
        object creation.

        """
        self._user_repository: IUserRepository = UserRepository(self.db)

    def create_user(self, user: UserCreate):
        """Creates a new user.

        Args:
            user (UserCreate): The user information.

        Raises:
            HTTPException: If the email is already registered.

        Returns:
            User: The created user.
        """
        db_user = self._user_repository.get_user_by_email(user.email)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        user_created = self._user_repository.create_user(user)
        return user_created

    def get_user(self, user_id: int):
        """Gets a user by id.

        Args:
            user_id (int): The user id.

        Raises:
            HTTPException: If the user is not found.

        Returns:
            User: The user information.
        """
        user = self._user_repository.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user

    def list_users(self):
        """Lists all users.

        Returns:
            A list of all users.

        """
        return self._user_repository.get_all_users()

    def update_user(self, user_id: int, user_update: UserUpdate):
        """Updates a user.

        Args:
            user_id (int): The id of the user to update.
            user_update (UserUpdate): The updated user data.

        Returns:
            The updated user.

        Raises:
            HTTPException: If the user is not found.

        """
        db_user = self._user_repository.get_user_by_id(user_id)

        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return self._user_repository.update_user(db_user, user_update)

    def delete_user(self, user_id: int):
        """Deletes a user.

        Args:
            user_id (int): The id of the user to delete.

        Returns:
            The deleted user.

        Raises:
            HTTPException: If the user is not found.

        """
        db_user = self._user_repository.get_user_by_id(user_id)

        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return self._user_repository.delete_user(db_user)

    async def reset_password_request(self, email: str, request: Request, background_tasks: BackgroundTasks) -> dict:
        """
        Sends a password reset link to the user's email address.

        Args:
            email (str): The email address of the user requesting a password reset.
            request (Request): The incoming request object.
            background_tasks (BackgroundTasks): The background task manager.

        Returns:
            dict: A dictionary with a "detail" key indicating the success of the password reset link send operation.

        Raises:
            HTTPException: If no user is found with the provided email address.
        """
        user = self._user_repository.get_user_by_email(email)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        jwt_token = self.token_manager.generate_jwt_token(user_email=user.email)
        html = self.templates.TemplateResponse(
            "password_reset_request.html",
            {"request": request, "jwt_token": jwt_token, "user_name": user.name},
        ).body
        await self.email_provider.send_email(
            recipients=[user.email],
            subject="Reset Password",
            body=html,
            subtype=MessageType.html,
            background_tasks=background_tasks,
        )
        return {"detail": "Password reset link sent successfully"}

    def reset_password(self, password_reset: PasswordReset):
        """
        Resets a user's password.

        Args:
            password_reset (PasswordReset): A `PasswordReset` object containing the password reset token and the new password.

        Returns:
            dict: A dictionary containing an "access_token" key with a JWT token for the user.

        Raises:
            HTTPException: If no user is found with the email address in the password reset token.
        """
        decoded_token = self.token_manager.decode_jwt_token(password_reset.token)
        user = self._user_repository.get_user_by_email(decoded_token["email"])

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        self._user_repository.update_user_password(user, password_reset.password)
        return {"access_token": self.token_manager.generate_jwt_token(user.email)}
