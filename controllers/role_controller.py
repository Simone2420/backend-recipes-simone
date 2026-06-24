from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from schemas.auth import RoleCreate, RoleUpdate, RoleResponse, PermissionCreate, PermissionUpdate, PermissionResponse
from repositories.role_repository import RoleRepository
from models.auth import User

class RoleController:
    @staticmethod
    def create_role(
        role_create: RoleCreate, 
        current_user: User, 
        db: Session
    ) -> RoleResponse:
        repo = RoleRepository(db)
        role = repo.create_role(role_create)
        return RoleResponse.model_validate(role)
    
    @staticmethod
    def get_role(
        role_id: int, 
        current_user: User, 
        db: Session
    ) -> RoleResponse:
        repo = RoleRepository(db)
        role = repo.get_role_by_id(role_id)
        if not role or not role.is_active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
        return RoleResponse.model_validate(role)
    
    @staticmethod
    def get_all_roles(
        current_user: User, 
        db: Session
    ) -> list[RoleResponse]:
        repo = RoleRepository(db)
        roles = repo.get_all_roles()
        return [RoleResponse.model_validate(role) for role in roles if role.is_active]
    
    @staticmethod
    def update_role(
        role_id: int, 
        role_update: RoleUpdate, 
        current_user: User, 
        db: Session
    ) -> RoleResponse:
        repo = RoleRepository(db)
        role = repo.get_role_by_id(role_id)
        if not role or not role.is_active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
        updated_role = repo.update_role(role, role_update)
        return RoleResponse.model_validate(updated_role)
    
    @staticmethod
    def delete_role(
        role_id: int, 
        current_user: User, 
        db: Session
    ) -> RoleResponse:
        repo = RoleRepository(db)
        role = repo.get_role_by_id(role_id)
        if not role or not role.is_active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
        deleted_role = repo.delete_role(role)
        return RoleResponse.model_validate(deleted_role)
    
    # --- Permission endpoints ---
    @staticmethod
    def create_permission(
        permission_create: PermissionCreate, 
        current_user: User, 
        db: Session
    ) -> PermissionResponse:
        repo = RoleRepository(db)
        permission = repo.create_permission(permission_create)
        return PermissionResponse.model_validate(permission)
    
    @staticmethod
    def get_all_permissions(
        current_user: User, 
        db: Session
    ) -> list[PermissionResponse]:
        repo = RoleRepository(db)
        permissions = repo.get_all_permissions()
        return [PermissionResponse.model_validate(p) for p in permissions]
