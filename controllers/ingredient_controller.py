from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile, File
from schemas.ingredients import IngredientCreate, IngredientUpdate, IngredientResponse
from repositories.ingredient_repository import IngredientRepository
from models.auth import User
from utilities.cloudinary import upload_image

class IngredientController:
    @staticmethod
    def create_ingredient(
        ingredient_create: IngredientCreate, 
        current_user: User, 
        db: Session
    ) -> IngredientResponse:
        repo = IngredientRepository(db)
        ingredient = repo.create_ingredient(ingredient_create)
        return IngredientResponse.model_validate(ingredient)
    
    @staticmethod
    def get_ingredient(ingredient_id: int, db: Session) -> IngredientResponse:
        repo = IngredientRepository(db)
        ingredient = repo.get_ingredient_by_id(ingredient_id)
        if not ingredient:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")
        return IngredientResponse.model_validate(ingredient)
    
    @staticmethod
    def get_all_ingredients(skip: int = 0, limit: int = 100, db: Session = None) -> list[IngredientResponse]:
        repo = IngredientRepository(db)
        ingredients = repo.get_all_ingredients(skip, limit)
        return [IngredientResponse.model_validate(ing) for ing in ingredients]
    
    @staticmethod
    def update_ingredient(
        ingredient_id: int, 
        ingredient_update: IngredientUpdate, 
        current_user: User, 
        db: Session
    ) -> IngredientResponse:
        repo = IngredientRepository(db)
        ingredient = repo.get_ingredient_by_id(ingredient_id)
        if not ingredient:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")
        updated_ingredient = repo.update_ingredient(ingredient, ingredient_update)
        return IngredientResponse.model_validate(updated_ingredient)
    
    @staticmethod
    def upload_ingredient_image(
        ingredient_id: int, 
        file: UploadFile, 
        current_user: User, 
        db: Session
    ) -> dict:
        repo = IngredientRepository(db)
        ingredient = repo.get_ingredient_by_id(ingredient_id)
        if not ingredient:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")
        image_url = upload_image(file)
        repo.add_ingredient_image(ingredient_id, image_url)
        return {"message": "Image uploaded successfully", "image_url": image_url}

