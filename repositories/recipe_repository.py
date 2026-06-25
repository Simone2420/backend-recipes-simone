from sqlalchemy.orm import Session
from models.recipes import Recipe, Difficulty, RecipeInfo, RecipeRating, RecipeImage
from models.steps import Step, StepImage
from models.ingredients import Ingredient, RecipeIngredient
from schemas.recipes import RecipeCreate, RecipeUpdate, DifficultyCreate, DifficultyUpdate
from schemas.steps import StepBase

class RecipeRepository:
    def __init__(self, db: Session):
        self.db = db
        
    # --- Difficulty ---
    def get_difficulty_by_id(self, difficulty_id: int) -> Difficulty:
        return self.db.query(Difficulty).filter(Difficulty.id == difficulty_id).first()
        
    def get_difficulty_by_name(self, name: str) -> Difficulty:
        return self.db.query(Difficulty).filter(Difficulty.name == name).first()
        
    def create_difficulty(self, difficulty: DifficultyCreate) -> Difficulty:
        new_diff = Difficulty(name=difficulty.name)
        self.db.add(new_diff)
        self.db.commit()
        self.db.refresh(new_diff)
        return new_diff

    def get_all_difficulties(self) -> list[Difficulty]:
        return self.db.query(Difficulty).all()

    # --- Recipe ---
    def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        return self.db.query(Recipe).filter(Recipe.id == recipe_id).first()
        
    def get_all_recipes(self, skip: int = 0, limit: int = 100) -> list[Recipe]:
        return self.db.query(Recipe).filter(Recipe.is_active == True).offset(skip).limit(limit).all()
        
    def get_recipes_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> list[Recipe]:
        return self.db.query(Recipe).filter(Recipe.user_id == user_id, Recipe.is_active == True).offset(skip).limit(limit).all()
        
    def create_recipe(self, recipe: RecipeCreate, user_id: int) -> Recipe:
        # 1. Create main Recipe object
        db_recipe = Recipe(
            name=recipe.name,
            description=recipe.description,
            difficulty_id=recipe.difficulty_id,
            user_id=user_id
        )
        self.db.add(db_recipe)
        self.db.commit()
        self.db.refresh(db_recipe)
        
        # 2. Add RecipeInfo if provided
        if recipe.info:
            db_info = RecipeInfo(
                recipe_id=db_recipe.id,
                prep_time=recipe.info.prep_time,
                cook_time=recipe.info.cook_time,
                total_time=recipe.info.total_time,
                calories=recipe.info.calories
            )
            self.db.add(db_info)
            
        # 3. Add Ingredients if provided
        for ing in recipe.ingredients:
            db_recipe_ing = RecipeIngredient(
                recipe_id=db_recipe.id,
                ingredient_id=ing.ingredient_id,
                quantity=ing.quantity,
                measurement_unit=ing.measurement_unit
            )
            self.db.add(db_recipe_ing)
            
        # 4. Add Steps if provided
        for step in recipe.steps:
            db_step = Step(
                recipe_id=db_recipe.id,
                content=step.content,
                description=step.description,
                order=step.order
            )
            self.db.add(db_step)
            
        self.db.commit()
        self.db.refresh(db_recipe)
        return db_recipe
        
    def update_recipe(self, db_recipe: Recipe, recipe_update: RecipeUpdate) -> Recipe:
        update_data = recipe_update.model_dump(exclude_unset=True)
        
        info_data = update_data.pop("info", None)
        ingredients_data = update_data.pop("ingredients", None)
        steps_data = update_data.pop("steps", None)

        for key, value in update_data.items():
            setattr(db_recipe, key, value)
            
        if info_data is not None:
            if db_recipe.infos:
                for k, v in info_data.items():
                    setattr(db_recipe.infos, k, v)
            else:
                db_info = RecipeInfo(recipe_id=db_recipe.id, **info_data)
                self.db.add(db_info)

        if ingredients_data is not None:
            self.db.query(RecipeIngredient).filter(RecipeIngredient.recipe_id == db_recipe.id).delete()
            for ing in ingredients_data:
                db_recipe_ing = RecipeIngredient(
                    recipe_id=db_recipe.id,
                    ingredient_id=ing["ingredient_id"],
                    quantity=ing["quantity"],
                    measurement_unit=ing["measurement_unit"]
                )
                self.db.add(db_recipe_ing)
                
        if steps_data is not None:
            existing_steps = {s.id: s for s in db_recipe.steps}
            updated_step_ids = set()
            
            for step_data in steps_data:
                step_id = step_data.get("id")
                if step_id and step_id in existing_steps:
                    step = existing_steps[step_id]
                    step.content = step_data["content"]
                    step.description = step_data.get("description")
                    step.order = step_data["order"]
                    updated_step_ids.add(step_id)
                else:
                    new_step = Step(
                        recipe_id=db_recipe.id,
                        content=step_data["content"],
                        description=step_data.get("description"),
                        order=step_data["order"]
                    )
                    self.db.add(new_step)
            
            for step_id, step in existing_steps.items():
                if step_id not in updated_step_ids:
                    self.db.delete(step)
                    
        self.db.commit()
        self.db.refresh(db_recipe)
        return db_recipe
        
    def delete_recipe(self, db_recipe: Recipe) -> Recipe:
        db_recipe.is_active = False
        self.db.commit()
        self.db.refresh(db_recipe)
        return db_recipe

    # --- Recipe Images ---
    def add_recipe_image(self, recipe_id: int, image_url: str) -> RecipeImage:
        db_img = RecipeImage(recipe_id=recipe_id, image_url=image_url)
        self.db.add(db_img)
        self.db.commit()
        self.db.refresh(db_img)
        return db_img

    # --- Recipe Ratings ---
    def add_recipe_rating(self, recipe_id: int, user_id: int, rating: int) -> RecipeRating:
        db_rating = RecipeRating(recipe_id=recipe_id, user_id=user_id, rating=rating)
        self.db.add(db_rating)
        self.db.commit()
        self.db.refresh(db_rating)
        return db_rating

    # --- Step Images ---
    def add_step_image(self, step_id: int, image_url: str) -> StepImage:
        db_img = StepImage(step_id=step_id, image_url=image_url)
        self.db.add(db_img)
        self.db.commit()
        self.db.refresh(db_img)
        return db_img
