from domain.ports.user_repository import UserRepository
from domain.services.token_service import TokenService
from infrastructure.adapters.password import verify_password
from application.dtos.user_login_dto import UserLogin
from application.dtos.token_dto import Token

class UserLoginUseCase:
    def __init__(self, user_repo: UserRepository, token_service: TokenService):
        self.user_repo = user_repo
        self.token_service = token_service

    def login(self, credentials: UserLogin) -> Token:
        user = self.user_repo.get_by_username(credentials.username)
        if not user or not verify_password(credentials.password, user.hashed_password):
            raise ValueError("Invalid credentials")

        access_token = self.token_service.create_access_token(
            data={"sub": user.username, "user_id": user.id}
        )
        return Token(access_token=access_token, token_type="bearer")