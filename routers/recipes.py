
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from config.database import get_db
from controllers.recipe_controller import RecipeController
from schemas.recipes import RecipeCreate, RecipeUpdate, RecipeResponse, DifficultyCreate, DifficultyResponse
from utilities.security import get_current_user, check_permission
from models.auth import User

router = APIRouter()

# --- Recipes ---
@router.post("/", response_model=RecipeResponse, status_code=201)
def create_recipe(recipe: RecipeCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), controller: RecipeController = Depends()):
    return controller.create_recipe(recipe, current_user, db)

@router.get("/", response_model=list[RecipeResponse])
def get_all_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), controller: RecipeController = Depends()):
    return controller.get_all_recipes(skip, limit, db)

@router.get("/my-recipes", response_model=list[RecipeResponse])
def get_user_recipes(skip: int = 0, limit: int = 100, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), controller: RecipeController = Depends()):
    return controller.get_user_recipes(skip, limit, current_user, db)

@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(recipe_id: int, db: Session = Depends(get_db), controller: RecipeController = Depends()):
    return controller.get_recipe(recipe_id, db)

@router.put("/{recipe_id}", response_model=RecipeResponse)
def update_recipe(recipe_id: int, recipe: RecipeUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), controller: RecipeController = Depends()):
    return controller.update_recipe(recipe_id, recipe, current_user, db)

@router.delete("/{recipe_id}", response_model=RecipeResponse)
def delete_recipe(recipe_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), controller: RecipeController = Depends()):
    return controller.delete_recipe(recipe_id, current_user, db)

@router.post("/{recipe_id}/rate")
def rate_recipe(recipe_id: int, rating: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), controller: RecipeController = Depends()):
    return controller.rate_recipe(recipe_id, rating, current_user, db)

@router.post("/{recipe_id}/image")
def upload_recipe_image(recipe_id: int, file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db), controller: RecipeController = Depends()):
    return controller.upload_recipe_image(recipe_id, file, current_user, db)

@router.post("/{recipe_id}/steps/{step_id}/image")
def upload_step_image(recipe_id: int, step_id: int, file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db), controller: RecipeController = Depends()):
    return controller.upload_step_image(recipe_id, step_id, file, current_user, db)


# --- Difficulties ---
@router.post("/difficulties/", response_model=DifficultyResponse, status_code=201)
def create_difficulty(difficulty: DifficultyCreate, current_user: User = Depends(check_permission("manage_difficulties")), db: Session = Depends(get_db), controller: RecipeController = Depends()):
    return controller.create_difficulty(difficulty, current_user, db)

@router.get("/difficulties/", response_model=list[DifficultyResponse])
def get_all_difficulties(db: Session = Depends(get_db), controller: RecipeController = Depends()):
    return controller.get_all_difficulties(db)

