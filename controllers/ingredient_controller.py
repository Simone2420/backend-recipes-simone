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
            
        # Verificar permisos: Admin o dueño de una receta que contenga este ingrediente
        is_admin = any(role.name.lower().startswith("admin") for role in current_user.roles)
        if not is_admin:
            from models.ingredients import RecipeIngredient
            from models.recipes import Recipe
            has_recipe = db.query(RecipeIngredient).join(Recipe).filter(
                RecipeIngredient.ingredient_id == ingredient_id,
                Recipe.user_id == current_user.id
            ).first() is not None
            if not has_recipe:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, 
                    detail="No tienes permiso para modificar este ingrediente porque no pertenece a tus recetas."
                )
                
        updated_ingredient = repo.update_ingredient(ingredient, ingredient_update)
        return IngredientResponse.model_validate(updated_ingredient)
    
    @staticmethod
    def delete_ingredient(
        ingredient_id: int, 
        current_user: User, 
        db: Session
    ) -> dict:
        repo = IngredientRepository(db)
        ingredient = repo.get_ingredient_by_id(ingredient_id)
        if not ingredient:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")
            
        is_admin = any(role.name.lower().startswith("admin") for role in current_user.roles)
        
        # Buscar vinculaciones en recetas del usuario actual
        from models.ingredients import RecipeIngredient
        from models.recipes import Recipe
        
        user_recipe_links = db.query(RecipeIngredient).join(Recipe).filter(
            RecipeIngredient.ingredient_id == ingredient_id,
            Recipe.user_id == current_user.id
        ).all()
        
        if is_admin:
            # Los administradores pueden borrar el ingrediente físicamente del catálogo
            repo.delete_ingredient(ingredient)
            return {"message": "Ingrediente eliminado físicamente del catálogo por el administrador."}
            
        if not user_recipe_links:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para eliminar este ingrediente porque no pertenece a tus recetas."
            )
            
        # Si no es admin y está en sus recetas: eliminamos solo los vínculos a sus recetas
        for link in user_recipe_links:
            db.delete(link)
        db.commit()
        
        return {"message": "Ingrediente removido de tus recetas. El ingrediente permanece en el catálogo general."}
    
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
            
        # Verificar permisos: Admin o dueño de una receta que contenga este ingrediente
        is_admin = any(role.name.lower().startswith("admin") for role in current_user.roles)
        if not is_admin:
            from models.ingredients import RecipeIngredient
            from models.recipes import Recipe
            has_recipe = db.query(RecipeIngredient).join(Recipe).filter(
                RecipeIngredient.ingredient_id == ingredient_id,
                Recipe.user_id == current_user.id
            ).first() is not None
            if not has_recipe:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, 
                    detail="No tienes permiso para subir imágenes a este ingrediente porque no pertenece a tus recetas."
                )
                
        image_url = upload_image(file)
        repo.add_ingredient_image(ingredient_id, image_url)
        return {"message": "Image uploaded successfully", "image_url": image_url}

