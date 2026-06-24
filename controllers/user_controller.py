from sqlalchemy.orm import Session
from services.user_service import UserService
from schemas.auth import UserUpdate, UserResponse
from models.auth import User

class UserController:
    @staticmethod
    def get_profile(current_user: User) -> UserResponse:
        return UserResponse.model_validate(current_user)
    
    @staticmethod
    def update_profile(
        user_update: UserUpdate, 
        current_user: User, 
        db: Session
    ) -> UserResponse:
        user = UserService.update_user_profile(db, current_user.id, user_update)
        return UserResponse.model_validate(user)
    
    @staticmethod
    def delete_account(
        current_user: User, 
        db: Session
    ) -> dict:
        UserService.delete_user_account(db, current_user.id)
        return {"message": "Account deleted successfully"}
    
    @staticmethod
    def get_user(
        user_id: int, 
        current_user: User, 
        db: Session
    ) -> UserResponse:
        user = UserService.get_user_profile(db, user_id)
        return UserResponse.model_validate(user)
    
    @staticmethod
    def assign_role(
        user_id: int, 
        role_id: int, 
        current_user: User, 
        db: Session
    ) -> UserResponse:
        user = UserService.assign_role_to_user(db, user_id, role_id)
        return UserResponse.model_validate(user)
    
    @staticmethod
    def remove_role(
        user_id: int, 
        role_id: int, 
        current_user: User, 
        db: Session
    ) -> UserResponse:
        user = UserService.remove_role_from_user(db, user_id, role_id)
        return UserResponse.model_validate(user)
