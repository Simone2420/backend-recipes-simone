
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from controllers.user_controller import UserController
from schemas.auth import UserUpdate, UserResponse
from utilities.security import get_current_user, check_permission
from models.auth import User

router = APIRouter()

# --- User's own profile ---
@router.get("/profile", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user), controller: UserController = Depends()):
    return controller.get_profile(current_user)

@router.put("/profile", response_model=UserResponse)
def update_profile(user: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), controller: UserController = Depends()):
    return controller.update_profile(user, current_user, db)

@router.delete("/profile")
def delete_account(current_user: User = Depends(get_current_user), db: Session = Depends(get_db), controller: UserController = Depends()):
    return controller.delete_account(current_user, db)

# --- Admin/User management ---
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, current_user: User = Depends(check_permission("view_users")), db: Session = Depends(get_db), controller: UserController = Depends()):
    return controller.get_user(user_id, current_user, db)

@router.post("/{user_id}/roles/{role_id}", response_model=UserResponse)
def assign_role(user_id: int, role_id: int, current_user: User = Depends(check_permission("manage_roles")), db: Session = Depends(get_db), controller: UserController = Depends()):
    return controller.assign_role(user_id, role_id, current_user, db)

@router.delete("/{user_id}/roles/{role_id}", response_model=UserResponse)
def remove_role(user_id: int, role_id: int, current_user: User = Depends(check_permission("manage_roles")), db: Session = Depends(get_db), controller: UserController = Depends()):
    return controller.remove_role(user_id, role_id, current_user, db)

