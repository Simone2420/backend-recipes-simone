import uuid
import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from repositories import UserRepository
from models.auth import Session as UserSession, User
from schemas.auth import UserCreate, UserLogin, TokenResponse
from utilities.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token
)
from config.jwt import SECRET_KEY, ALGORITHM

class AuthService:
    @staticmethod
    def signup_user(db: Session, user_create: UserCreate) -> User:
        """Handles user registration, hashes the password, and saves the user."""
        repo = UserRepository(db)
        # Check if user already exists
        if repo.get_user_by_email(user_create.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered"
            )
            
        # Hash the password
        hashed_password = get_password_hash(user_create.password)
        # Create a new create schema with hashed password
        db_user_data = UserCreate(
            username=user_create.username,
            email=user_create.email,
            password=hashed_password
        )
        return repo.create_user(db_user_data)

    @staticmethod
    def login_user(db: Session, user_login: UserLogin) -> TokenResponse:
        """Authenticates user, creates access and refresh tokens, and registers the session."""
        repo = UserRepository(db)
        user = repo.get_user_by_email(user_login.email)
        
        if not user or not verify_password(user_login.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User account is inactive"
            )

        # Generate unique identifiers (jti) for access and refresh tokens
        access_jti = uuid.uuid4().hex
        refresh_jti = uuid.uuid4().hex
        
        # Calculate expiration times
        # Default access token expires in 24 hours (1440 minutes), refresh in 7 days
        access_expires = timedelta(minutes=1440)
        refresh_expires = timedelta(days=7)
        
        access_token = create_access_token(
            data={"sub": user.email, "jti": access_jti},
            expires_delta=access_expires
        )
        refresh_token = create_refresh_token(
            data={"sub": user.email, "jti": refresh_jti},
            expires_delta=refresh_expires
        )
        
        # Save sessions to DB
        access_session = UserSession(
            user_id=user.id,
            jti=access_jti,
            expires_at=datetime.utcnow() + access_expires
        )
        refresh_session = UserSession(
            user_id=user.id,
            jti=refresh_jti,
            expires_at=datetime.utcnow() + refresh_expires
        )
        
        db.add(access_session)
        db.add(refresh_session)
        db.commit()
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )

    @staticmethod
    def refresh_token(db: Session, refresh_token_str: str) -> TokenResponse:
        """Verifies a refresh token and generates a new access token and fresh refresh token."""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(refresh_token_str, SECRET_KEY, algorithms=[ALGORITHM])
            email_str: str = payload.get("sub")
            jti: str = payload.get("jti")
            token_type: str = payload.get("type")
            
            if email_str is None or jti is None or token_type != "refresh":
                raise credentials_exception
                
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.PyJWTError:
            raise credentials_exception
            
        # Check if the refresh session exists and is not revoked
        session = db.query(UserSession).filter(UserSession.jti == jti).first()
        if not session or session.revoked or session.expires_at < datetime.utcnow():
            raise credentials_exception
            
        user = db.query(User).filter(User.id == session.user_id).first()
        if not user or not user.is_active:
            raise credentials_exception
            
        # Revoke the old refresh token (single use refresh token rotation)
        session.revoked = True
        
        # Generate new tokens
        access_jti = uuid.uuid4().hex
        refresh_jti = uuid.uuid4().hex
        
        access_expires = timedelta(minutes=1440)
        refresh_expires = timedelta(days=7)
        
        new_access_token = create_access_token(
            data={"sub": user.email, "jti": access_jti},
            expires_delta=access_expires
        )
        new_refresh_token = create_refresh_token(
            data={"sub": user.email, "jti": refresh_jti},
            expires_delta=refresh_expires
        )
        
        # Save new sessions
        new_access_session = UserSession(
            user_id=user.id,
            jti=access_jti,
            expires_at=datetime.utcnow() + access_expires
        )
        new_refresh_session = UserSession(
            user_id=user.id,
            jti=refresh_jti,
            expires_at=datetime.utcnow() + refresh_expires
        )
        
        db.add(new_access_session)
        db.add(new_refresh_session)
        db.commit()
        
        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )

    @staticmethod
    def logout_user(db: Session, jti: str) -> None:
        """Revokes a session by marking its JTI as revoked."""
        session = db.query(UserSession).filter(UserSession.jti == jti).first()
        if session:
            session.revoked = True
            db.commit()

    @staticmethod
    def is_token_revoked(db: Session, jti: str) -> bool:
        """Checks if a JTI has been revoked or expired."""
        session = db.query(UserSession).filter(UserSession.jti == jti).first()
        if not session:
            return True
        return session.revoked or session.expires_at < datetime.utcnow()
