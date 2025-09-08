from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from infrastructure.adapters.database import SessionLocal, Base, engine
from infrastructure.adapters.repositories import SQLUserRepository
from infrastructure.adapters.jwt import JWTService
from application.services.user_login import UserLoginUseCase
from application.services.user_registration import UserRegistrationUseCase
from application.dtos import UserCreate, UserLogin, Token
from infrastructure.adapters.logging import logger

app = FastAPI(
    title="bk users",
    description="Servicio de autenticacion y gestion de usuarios",
    version="1.0.0"
)

# creacion schema
Base.metadata.create_all(bind=engine)

# necesario para fastapi
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register", response_model=Token, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    logger.info("register_attempt", username=user.username)
    try:
        repo = SQLUserRepository(db)
        token_service = JWTService()
        use_case = UserRegistrationUseCase(repo, token_service)
        token = use_case.register(user)
        logger.info("user_registered", username=user.username)
        return token
    except ValueError as e:
        logger.warn("register_failed", username=user.username, error=str(e))
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    logger.info("login_attempt", username=credentials.username)
    try:
        repo = SQLUserRepository(db)
        token_service = JWTService()
        use_case = UserLoginUseCase(repo, token_service)
        token = use_case.login(credentials)
        logger.info("user_logged_in", username=credentials.username)
        return token
    except ValueError as e:
        logger.warn("login_failed", username=credentials.username, error=str(e))
        raise HTTPException(status_code=401, detail="Invalid credentials")

# Endpoint interno para validación de token (usado por transacciones-service)
@app.get("/validate-token")
def validate_token(token: str, db: Session = Depends(get_db)):
    logger.info("token_validation_attempt", token_preview=token[:10] + "...")
    try:
        token_service = JWTService()
        payload = token_service.verify_token(token)
        user_id = payload.get("user_id")

        if not user_id:
            raise ValueError("User ID not found in token")

        repo = SQLUserRepository(db)
        user = repo.get_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        logger.info("token_validated", user_id=user.id, username=user.username)
        return {
            "user_id": user.id,
            "username": user.username,
            "email": user.email
        }
    except Exception as e:
        logger.error("token_validation_failed", error=str(e))
        raise HTTPException(status_code=401, detail="Invalid or expired token")