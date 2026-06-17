from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Step Images
class StepImageBase(BaseModel):
    image_url: str

class StepImageCreate(StepImageBase):
    step_id: int

class StepImageResponse(StepImageBase):
    id: int
    step_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Steps
class StepBase(BaseModel):
    content: str
    description: Optional[str] = None
    order: int

class StepCreate(StepBase):
    recipe_id: int

class StepUpdate(BaseModel):
    content: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None

class StepResponse(StepBase):
    id: int
    recipe_id: int
    created_at: datetime
    updated_at: datetime
    images: List[StepImageResponse] = []

    class Config:
        from_attributes = True
