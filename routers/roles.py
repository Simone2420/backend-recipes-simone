
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from controllers.role_controller import RoleController
from schemas.auth import RoleCreate, RoleUpdate, RoleResponse, PermissionCreate, PermissionResponse
from utilities.security import check_permission
from models.auth import User

router = APIRouter()

# --- Roles ---
@router.post("/", response_model=RoleResponse, status_code=201)
def create_role(role: RoleCreate, current_user: User = Depends(check_permission("manage_roles")), db: Session = Depends(get_db), controller: RoleController = Depends()):
    return controller.create_role(role, current_user, db)

@router.get("/", response_model=list[RoleResponse])
def get_all_roles(current_user: User = Depends(check_permission("view_roles")), db: Session = Depends(get_db), controller: RoleController = Depends()):
    return controller.get_all_roles(current_user, db)

@router.get("/{role_id}", response_model=RoleResponse)
def get_role(role_id: int, current_user: User = Depends(check_permission("view_roles")), db: Session = Depends(get_db), controller: RoleController = Depends()):
    return controller.get_role(role_id, current_user, db)

@router.put("/{role_id}", response_model=RoleResponse)
def update_role(role_id: int, role: RoleUpdate, current_user: User = Depends(check_permission("manage_roles")), db: Session = Depends(get_db), controller: RoleController = Depends()):
    return controller.update_role(role_id, role, current_user, db)

@router.delete("/{role_id}", response_model=RoleResponse)
def delete_role(role_id: int, current_user: User = Depends(check_permission("manage_roles")), db: Session = Depends(get_db), controller: RoleController = Depends()):
    return controller.delete_role(role_id, current_user, db)

# --- Permissions ---
@router.post("/permissions/", response_model=PermissionResponse, status_code=201)
def create_permission(permission: PermissionCreate, current_user: User = Depends(check_permission("manage_permissions")), db: Session = Depends(get_db), controller: RoleController = Depends()):
    return controller.create_permission(permission, current_user, db)

@router.get("/permissions/", response_model=list[PermissionResponse])
def get_all_permissions(current_user: User = Depends(check_permission("view_permissions")), db: Session = Depends(get_db), controller: RoleController = Depends()):
    return controller.get_all_permissions(current_user, db)

