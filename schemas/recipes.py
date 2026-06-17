from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from schemas.auth import UserResponse
from schemas.ingredients import RecipeIngredientDetailResponse, RecipeIngredientCreate
from schemas.steps import StepResponse, StepBase

# Difficulty
class DifficultyBase(BaseModel):
    name: str

class DifficultyCreate(DifficultyBase):
    pass

class DifficultyUpdate(BaseModel):
    name: Optional[str] = None

class DifficultyResponse(DifficultyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Recipe Info
class RecipeInfoBase(BaseModel):
    prep_time: int
    cook_time: int
    total_time: int
    calories: int

class RecipeInfoCreate(RecipeInfoBase):
    recipe_id: int

class RecipeInfoUpdate(BaseModel):
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    total_time: Optional[int] = None
    calories: Optional[int] = None

class RecipeInfoResponse(RecipeInfoBase):
    id: int
    recipe_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Recipe Ratings
class RecipeRatingBase(BaseModel):
    rating: int

class RecipeRatingCreate(RecipeRatingBase):
    recipe_id: int

class RecipeRatingResponse(RecipeRatingBase):
    id: int
    recipe_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Recipe Images
class RecipeImageBase(BaseModel):
    image_url: str

class RecipeImageCreate(RecipeImageBase):
    recipe_id: int

class RecipeImageResponse(RecipeImageBase):
    id: int
    recipe_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Recipe
class RecipeBase(BaseModel):
    name: str
    description: str

class RecipeCreate(RecipeBase):
    difficulty_id: int
    info: Optional[RecipeInfoBase] = None
    ingredients: List[RecipeIngredientCreate] = []
    steps: List[StepBase] = []

class RecipeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    difficulty_id: Optional[int] = None
    is_active: Optional[bool] = None

class RecipeResponse(RecipeBase):
    id: int
    difficulty_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    user_id: int
    
    user: Optional[UserResponse] = None
    difficulty: Optional[DifficultyResponse] = None
    infos: Optional[RecipeInfoResponse] = None
    images: List[RecipeImageResponse] = []
    ratings: List[RecipeRatingResponse] = []
    ingredients: List[RecipeIngredientDetailResponse] = []
    steps: List[StepResponse] = []

    class Config:
        from_attributes = True
