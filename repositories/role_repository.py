from sqlalchemy.orm import Session
from models import Role, Permission
from schemas.auth import RoleCreate, RoleUpdate, PermissionCreate, PermissionUpdate

class RoleRepository:
    def __init__(self, db: Session):
        self.db = db
    
    # --- Roles ---
    def get_role_by_id(self, role_id: int) -> Role:
        return self.db.query(Role).filter(Role.id == role_id).first()
        
    def get_role_by_name(self, name: str) -> Role:
        return self.db.query(Role).filter(Role.name == name).first()
        
    def create_role(self, role: RoleCreate) -> Role:
        new_role = Role(
            name=role.name,
            description=role.description,
        )
        self.db.add(new_role)
        self.db.commit()
        self.db.refresh(new_role)
        return new_role
        
    def update_role(self, db_role: Role, role_update: RoleUpdate) -> Role:
        update_data = role_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_role, key, value)
        self.db.commit()
        self.db.refresh(db_role)
        return db_role
        
    def delete_role(self, db_role: Role) -> Role:
        db_role.is_active = False
        self.db.commit()
        self.db.refresh(db_role)
        return db_role
        
    def get_all_roles(self) -> list[Role]:
        return self.db.query(Role).all()

    # --- Permissions ---
    def get_permission_by_id(self, permission_id: int) -> Permission:
        return self.db.query(Permission).filter(Permission.id == permission_id).first()
        
    def get_permission_by_name(self, name: str) -> Permission:
        return self.db.query(Permission).filter(Permission.name == name).first()
        
    def create_permission(self, permission: PermissionCreate) -> Permission:
        new_perm = Permission(
            name=permission.name,
            description=permission.description,
        )
        self.db.add(new_perm)
        self.db.commit()
        self.db.refresh(new_perm)
        return new_perm
        
    def update_permission(self, db_permission: Permission, permission_update: PermissionUpdate) -> Permission:
        update_data = permission_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_permission, key, value)
        self.db.commit()
        self.db.refresh(db_permission)
        return db_permission
        
    def get_all_permissions(self) -> list[Permission]:
        return self.db.query(Permission).all()