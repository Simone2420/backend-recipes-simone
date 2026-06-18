from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.recipe_repository import RecipeRepository
from models.recipes import Recipe, RecipeRating
from schemas.recipes import RecipeCreate, RecipeUpdate

class RecipeService:
    @staticmethod
    def create_recipe(db: Session, recipe_create: RecipeCreate, user_id: int) -> Recipe:
        """Business logic for creating a new recipe with nested step and ingredient details."""
        repo = RecipeRepository(db)
        return repo.create_recipe(recipe_create, user_id)

    @staticmethod
    def get_recipe(db: Session, recipe_id: int) -> Recipe:
        """Retrieves a recipe by ID, raising an exception if not found."""
        repo = RecipeRepository(db)
        recipe = repo.get_recipe_by_id(recipe_id)
        if not recipe or not recipe.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found"
            )
        return recipe

    @staticmethod
    def get_all_recipes(db: Session, skip: int = 0, limit: int = 100) -> list[Recipe]:
        """Lists active recipes."""
        repo = RecipeRepository(db)
        return repo.get_all_recipes(skip, limit)

    @staticmethod
    def get_user_recipes(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Recipe]:
        """Lists active recipes created by a specific user."""
        repo = RecipeRepository(db)
        return repo.get_recipes_by_user(user_id, skip, limit)

    @staticmethod
    def update_recipe(db: Session, recipe_id: int, recipe_update: RecipeUpdate, current_user_id: int, is_admin: bool = False) -> Recipe:
        """Updates a recipe if the user owns it or is an admin."""
        repo = RecipeRepository(db)
        recipe = repo.get_recipe_by_id(recipe_id)
        
        if not recipe or not recipe.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found"
            )
            
        if recipe.user_id != current_user_id and not is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this recipe"
            )
            
        return repo.update_recipe(recipe, recipe_update)

    @staticmethod
    def delete_recipe(db: Session, recipe_id: int, current_user_id: int, is_admin: bool = False) -> Recipe:
        """Soft deletes a recipe if the user owns it or is an admin."""
        repo = RecipeRepository(db)
        recipe = repo.get_recipe_by_id(recipe_id)
        
        if not recipe or not recipe.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found"
            )
            
        if recipe.user_id != current_user_id and not is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this recipe"
            )
            
        return repo.delete_recipe(recipe)

    @staticmethod
    def rate_recipe(db: Session, recipe_id: int, user_id: int, rating: int) -> RecipeRating:
        """Rates a recipe (verifying rating ranges and recipe existence)."""
        if rating < 1 or rating > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rating must be an integer between 1 and 5"
            )
            
        repo = RecipeRepository(db)
        recipe = repo.get_recipe_by_id(recipe_id)
        if not recipe or not recipe.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found"
            )
            
        # Check if user has already rated this recipe
        db_rating = db.query(RecipeRating).filter(
            RecipeRating.recipe_id == recipe_id,
            RecipeRating.user_id == user_id
        ).first()
        
        if db_rating:
            db_rating.rating = rating
            db.commit()
            db.refresh(db_rating)
            return db_rating
            
        return repo.add_recipe_rating(recipe_id, user_id, rating)

    @staticmethod
    def add_recipe_image(db: Session, recipe_id: int, image_url: str, current_user_id: int, is_admin: bool = False) -> str:
        """Associates an uploaded image URL with a recipe."""
        repo = RecipeRepository(db)
        recipe = repo.get_recipe_by_id(recipe_id)
        
        if not recipe or not recipe.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found"
            )
            
        if recipe.user_id != current_user_id and not is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to modify this recipe"
            )
            
        repo.add_recipe_image(recipe_id, image_url)
        return image_url
