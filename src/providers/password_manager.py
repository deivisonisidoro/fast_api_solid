from passlib.context import CryptContext

from .interfaces.ipassword_manager import IPasswordManager


class PasswordManager(IPasswordManager):
    def __init__(self, pwd_context: CryptContext = CryptContext(schemes=["bcrypt"])):
        self.pwd_context = pwd_context

    def hash_generate(self, text: str) -> str:
        return self.pwd_context.hash(text)

    def hash_verify(self, text, hash) -> bool:
        return self.pwd_context.verify(text, hash)
