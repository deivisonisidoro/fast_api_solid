from abc import ABC, abstractmethod


class ITokenManager(ABC):
    @abstractmethod
    def create_access_token(self, data: dict) -> str:
        pass

    @abstractmethod
    def verify_access_token(self, token: str) -> str:
        pass
