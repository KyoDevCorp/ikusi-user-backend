from sqlalchemy.orm import Session
from domain.ports.user_repository import UserRepository
from domain.entities.user import User
from .database import UserDB

class SQLUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        db_user = UserDB(
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active
        )
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)

        return User(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            hashed_password=db_user.hashed_password,
            is_active=db_user.is_active
        )

    def get_by_username(self, username: str) -> User | None:
        db_user = self.session.query(UserDB).filter(UserDB.username == username).first()
        if db_user:
            return User(
                id=db_user.id,
                username=db_user.username,
                email=db_user.email,
                hashed_password=db_user.hashed_password,
                is_active=db_user.is_active
            )
        return None

    def get_by_id(self, user_id: int) -> User | None:
        db_user = self.session.query(UserDB).filter(UserDB.id == user_id).first()
        if db_user:
            return User(
                id=db_user.id,
                username=db_user.username,
                email=db_user.email,
                hashed_password=db_user.hashed_password,
                is_active=db_user.is_active
            )
        return None