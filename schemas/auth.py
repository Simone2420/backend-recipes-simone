from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class PermissionCreate(BaseModel):
    name: str
    description: Optional[str] = None

class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class RolePermissionCreate(BaseModel):
    role_id: int
    permission_id: int

class RolePermissionUpdate(BaseModel):
    role_id: Optional[int] = None
    permission_id: Optional[int] = None
        
class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime    
    
    class Config:
        from_attributes = True

class PermissionResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime    
    
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool = True
    created_at: datetime
    updated_at: datetime    
    roles: List[RoleResponse] = []

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    username: Optional[str] = None
    jti: Optional[str] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    
    class Config:
        from_attributes = True

class TokenRefresh(BaseModel):
    refresh_token: str
    
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    
    class Config:
        from_attributes = True

