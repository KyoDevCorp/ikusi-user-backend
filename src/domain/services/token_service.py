from abc import ABC, abstractmethod

class TokenService(ABC):
    @abstractmethod
    def create_access_token(self,  dict) -> str:
        pass

    @abstractmethod
    def verify_token(self, token: str) -> dict:
        pass