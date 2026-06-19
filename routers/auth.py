
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from controllers.auth_controller import AuthController
from schemas.auth import UserCreate, UserLogin, TokenResponse, UserResponse, TokenRefresh
from utilities.security import get_current_user
from models.auth import User

router = APIRouter()

@router.post("/signup", response_model=UserResponse, status_code=201)
def signup(user: UserCreate, db: Session = Depends(get_db), controller: AuthController = Depends()):
    return controller.signup(user, db)

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db), controller: AuthController = Depends()):
    return controller.login(user, db)

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(token: TokenRefresh, db: Session = Depends(get_db), controller: AuthController = Depends()):
    return controller.refresh_token(token.refresh_token, db)

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user), db: Session = Depends(get_db), controller: AuthController = Depends()):
    return controller.logout(current_user, db)

