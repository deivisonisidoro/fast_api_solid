from passlib.context import CryptContext

from .interfaces.ipassword_manager import IPasswordManagerProvider


class PasswordManagerProvider(IPasswordManagerProvider):
    """
    Implementation of IPasswordManagerProvider that uses PassLib to hash and verify passwords.

    Args:
        pwd_context (CryptContext): An instance of passlib's CryptContext. Default is a CryptContext instance using the bcrypt scheme.
    """

    def __init__(self, pwd_context: CryptContext = CryptContext(schemes=["bcrypt"])):
        self.pwd_context = pwd_context

    def hash_generate(self, text: str) -> str:
        """
        Hashes a password string.

        Args:
            text (str): The password string to be hashed.

        Returns:
            str: The hashed password.
        """
        return self.pwd_context.hash(text)

    def hash_verify(self, text, hash) -> bool:
        """
        Verifies a password string against a hash.

        Args:
            text (str): The password string to be verified.
            hash: The hash string to be compared against.

        Returns:
            bool: True if the password matches the hash, False otherwise.
        """
        return self.pwd_context.verify(text, hash)
