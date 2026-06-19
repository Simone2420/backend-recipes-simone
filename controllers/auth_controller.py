from sqlalchemy.orm import Session
from services.auth_service import AuthService
from schemas.auth import UserCreate, UserLogin, TokenResponse, UserResponse
from models.auth import User

class AuthController:
    @staticmethod
    def signup(user_create: UserCreate, db: Session) -> UserResponse:
        user = AuthService.signup_user(db, user_create)
        return UserResponse.model_validate(user)
    
    @staticmethod
    def login(user_login: UserLogin, db: Session) -> TokenResponse:
        return AuthService.login_user(db, user_login)
    
    @staticmethod
    def refresh_token(refresh_token: str, db: Session) -> TokenResponse:
        return AuthService.refresh_token(db, refresh_token)
    
    @staticmethod
    def logout(current_user: User, db: Session) -> dict:
        AuthService.logout_user(db, current_user.current_jti)
        return {"message": "Successfully logged out"}
