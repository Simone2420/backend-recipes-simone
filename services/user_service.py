from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.user_repository import UserRepository
from repositories.role_repository import RoleRepository
from models.auth import User, Role
from schemas.auth import UserUpdate

class UserService:
    @staticmethod
    def get_user_profile(db: Session, user_id: int) -> User:
        """Retrieves user profile, raising 404 if not found."""
        repo = UserRepository(db)
        user = repo.get_user_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    @staticmethod
    def update_user_profile(db: Session, user_id: int, user_update: UserUpdate) -> User:
        """Updates user profile details."""
        repo = UserRepository(db)
        user = repo.get_user_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return repo.update_user(user, user_update)

    @staticmethod
    def delete_user_account(db: Session, user_id: int) -> User:
        """Soft deletes user account."""
        repo = UserRepository(db)
        user = repo.get_user_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return repo.delete_user(user)

    @staticmethod
    def assign_role_to_user(db: Session, user_id: int, role_id: int) -> User:
        """Assigns a role to a user (RBAC management)."""
        user_repo = UserRepository(db)
        role_repo = RoleRepository(db)
        
        user = user_repo.get_user_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        role = role_repo.get_role_by_id(role_id)
        if not role or not role.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
            
        if role not in user.roles:
            user.roles.append(role)
            db.commit()
            db.refresh(user)
            
        return user

    @staticmethod
    def remove_role_from_user(db: Session, user_id: int, role_id: int) -> User:
        """Removes a role from a user (RBAC management)."""
        user_repo = UserRepository(db)
        role_repo = RoleRepository(db)
        
        user = user_repo.get_user_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        role = role_repo.get_role_by_id(role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
            
        if role in user.roles:
            user.roles.remove(role)
            db.commit()
            db.refresh(user)
            
        return user
