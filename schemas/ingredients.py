from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Ingredient Images
class IngredientImageBase(BaseModel):
    image_url: str

class IngredientImageCreate(IngredientImageBase):
    ingredient_id: int

class IngredientImageResponse(IngredientImageBase):
    id: int
    ingredient_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Ingredients
class IngredientBase(BaseModel):
    name: str

class IngredientCreate(IngredientBase):
    pass

class IngredientUpdate(BaseModel):
    name: Optional[str] = None

class IngredientResponse(IngredientBase):
    id: int
    created_at: datetime
    updated_at: datetime
    images: List[IngredientImageResponse] = []

    class Config:
        from_attributes = True

# Recipe Ingredients (association table schemas)
class RecipeIngredientBase(BaseModel):
    quantity: str
    measurement_unit: str

class RecipeIngredientCreate(RecipeIngredientBase):
    ingredient_id: int

class RecipeIngredientUpdate(BaseModel):
    quantity: Optional[str] = None
    measurement_unit: Optional[str] = None

class RecipeIngredientResponse(RecipeIngredientBase):
    id: int
    recipe_id: int
    ingredient_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# For nested display of ingredients in a Recipe Response
class RecipeIngredientDetailResponse(RecipeIngredientBase):
    id: int
    ingredient_id: int
    name: str
    images: List[IngredientImageResponse] = []

    class Config:
        from_attributes = True
