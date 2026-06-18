from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from schemas.auth import UserResponse

class CommentBase(BaseModel):
    title: str
    comment: str

class CommentCreate(CommentBase):
    recipe_id: int

class CommentUpdate(BaseModel):
    title: Optional[str] = None
    comment: Optional[str] = None
    is_active: Optional[bool] = None

class CommentResponse(CommentBase):
    id: int
    recipe_id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    user: Optional[UserResponse] = None

    class Config:
        from_attributes = True
