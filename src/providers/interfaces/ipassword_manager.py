from abc import ABC, abstractmethod


class IPasswordManagerProvider(ABC):
    @abstractmethod
    def hash_generate(self, text: str) -> str:
        pass

    @abstractmethod
    def hash_verify(self, text: str, hash: str) -> bool:
        pass
