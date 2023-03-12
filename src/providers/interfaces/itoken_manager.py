from abc import ABC, abstractmethod


class ITokenManagerProvider(ABC):
    @abstractmethod
    def create_access_token(self, data: dict) -> str:
        pass

    @abstractmethod
    def generate_jwt_token(self, user_email: str) -> str:
        pass

    @abstractmethod
    def decode_jwt_token(self, encoded_jwt_token: str) -> dict[str, any]:
        pass

    @abstractmethod
    def verify_access_token(self, token: str) -> str:
        pass
