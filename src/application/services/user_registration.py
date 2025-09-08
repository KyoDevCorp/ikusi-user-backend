from domain.ports.user_repository import UserRepository
from domain.services.token_service import TokenService
from infrastructure.adapters.password import get_password_hash
from application.dtos.user_create_dto import UserCreate
from application.dtos.token_dto import Token
from domain.entities.user import User

class UserRegistrationUseCase:
    def __init__(self, user_repo: UserRepository, token_service: TokenService):
        self.user_repo = user_repo
        self.token_service = token_service

    def register(self, user_data: UserCreate) -> Token:
        # Verificar si ya existe
        if self.user_repo.get_by_username(user_data.username):
            raise ValueError("Username already registered")

        # Hashear contraseña
        hashed_pw = get_password_hash(user_data.password)

        # Crear usuario
        user = User(
            id=0,
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_pw
        )

        # Guardar en repositorio
        saved_user = self.user_repo.create(user)

        # Generar token
        access_token = self.token_service.create_access_token(
            data={"sub": saved_user.username, "user_id": saved_user.id}
        )

        return Token(access_token=access_token, token_type="bearer")