from sqlalchemy.orm import Session
from fastapi import UploadFile, File
from services.recipe_service import RecipeService
from schemas.recipes import RecipeCreate, RecipeUpdate, RecipeResponse, DifficultyCreate, DifficultyResponse
from models.auth import User
from repositories.recipe_repository import RecipeRepository
from utilities.cloudinary import upload_image

class RecipeController:
    @staticmethod
    def create_recipe(
        recipe_create: RecipeCreate, 
        current_user: User, 
        db: Session
    ) -> RecipeResponse:
        recipe = RecipeService.create_recipe(db, recipe_create, current_user.id)
        return RecipeResponse.model_validate(recipe)
    
    @staticmethod
    def get_recipe(recipe_id: int, db: Session) -> RecipeResponse:
        recipe = RecipeService.get_recipe(db, recipe_id)
        return RecipeResponse.model_validate(recipe)
    
    @staticmethod
    def get_all_recipes(skip: int = 0, limit: int = 100, db: Session = None) -> list[RecipeResponse]:
        recipes = RecipeService.get_all_recipes(db, skip, limit)
        return [RecipeResponse.model_validate(recipe) for recipe in recipes]
    
    @staticmethod
    def get_user_recipes(
        skip: int = 0, 
        limit: int = 100, 
        current_user: User = None, 
        db: Session = None
    ) -> list[RecipeResponse]:
        recipes = RecipeService.get_user_recipes(db, current_user.id, skip, limit)
        return [RecipeResponse.model_validate(recipe) for recipe in recipes]
    
    @staticmethod
    def update_recipe(
        recipe_id: int, 
        recipe_update: RecipeUpdate, 
        current_user: User, 
        db: Session
    ) -> RecipeResponse:
        is_admin = any(role.name.lower() == "admin" for role in current_user.roles)
        recipe = RecipeService.update_recipe(db, recipe_id, recipe_update, current_user.id, is_admin)
        return RecipeResponse.model_validate(recipe)
    
    @staticmethod
    def delete_recipe(
        recipe_id: int, 
        current_user: User, 
        db: Session
    ) -> RecipeResponse:
        is_admin = any(role.name.lower() == "admin" for role in current_user.roles)
        recipe = RecipeService.delete_recipe(db, recipe_id, current_user.id, is_admin)
        return RecipeResponse.model_validate(recipe)
    
    @staticmethod
    def rate_recipe(
        recipe_id: int, 
        rating: int, 
        current_user: User, 
        db: Session
    ) -> dict:
        RecipeService.rate_recipe(db, recipe_id, current_user.id, rating)
        return {"message": "Rating added successfully", "rating": rating}
    
    @staticmethod
    def upload_recipe_image(
        recipe_id: int, 
        file: UploadFile, 
        current_user: User, 
        db: Session
    ) -> dict:
        image_url = upload_image(file)
        is_admin = any(role.name.lower() == "admin" for role in current_user.roles)
        RecipeService.add_recipe_image(db, recipe_id, image_url, current_user.id, is_admin)
        return {"message": "Image uploaded successfully", "image_url": image_url}

    @staticmethod
    def upload_step_image(
        recipe_id: int, 
        step_id: int,
        file: UploadFile, 
        current_user: User, 
        db: Session
    ) -> dict:
        image_url = upload_image(file)
        is_admin = any(role.name.lower() == "admin" for role in current_user.roles)
        RecipeService.add_step_image(db, recipe_id, step_id, image_url, current_user.id, is_admin)
        return {"message": "Step image uploaded successfully", "image_url": image_url}
    
    # --- Difficulty endpoints ---
    @staticmethod
    def create_difficulty(
        difficulty_create: DifficultyCreate, 
        current_user: User, 
        db: Session
    ) -> DifficultyResponse:
        repo = RecipeRepository(db)
        difficulty = repo.create_difficulty(difficulty_create)
        return DifficultyResponse.model_validate(difficulty)
    
    @staticmethod
    def get_all_difficulties(db: Session) -> list[DifficultyResponse]:
        repo = RecipeRepository(db)
        difficulties = repo.get_all_difficulties()
        return [DifficultyResponse.model_validate(d) for d in difficulties]
