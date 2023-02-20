from abc import ABC, abstractmethod


class IPasswordManager(ABC):
    @abstractmethod
    def hash_generate(self, text: str) -> str:
        pass

    @abstractmethod
    def hash_verify(self, text: str, hash: str) -> bool:
        pass
