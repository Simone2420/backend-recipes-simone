
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from config.database import get_db
from controllers.ingredient_controller import IngredientController
from schemas.ingredients import IngredientCreate, IngredientUpdate, IngredientResponse
from utilities.security import check_permission
from models.auth import User

router = APIRouter()

@router.post("/", response_model=IngredientResponse, status_code=201)
def create_ingredient(ingredient: IngredientCreate, current_user: User = Depends(check_permission("manage_ingredients")), db: Session = Depends(get_db), controller: IngredientController = Depends()):
    return controller.create_ingredient(ingredient, current_user, db)

@router.get("/", response_model=list[IngredientResponse])
def get_all_ingredients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), controller: IngredientController = Depends()):
    return controller.get_all_ingredients(skip, limit, db)

@router.get("/{ingredient_id}", response_model=IngredientResponse)
def get_ingredient(ingredient_id: int, db: Session = Depends(get_db), controller: IngredientController = Depends()):
    return controller.get_ingredient(ingredient_id, db)

@router.put("/{ingredient_id}", response_model=IngredientResponse)
def update_ingredient(ingredient_id: int, ingredient: IngredientUpdate, current_user: User = Depends(check_permission("manage_ingredients")), db: Session = Depends(get_db), controller: IngredientController = Depends()):
    return controller.update_ingredient(ingredient_id, ingredient, current_user, db)

@router.post("/{ingredient_id}/image")
def upload_ingredient_image(ingredient_id: int, file: UploadFile = File(...), current_user: User = Depends(check_permission("manage_ingredients")), db: Session = Depends(get_db), controller: IngredientController = Depends()):
    return controller.upload_ingredient_image(ingredient_id, file, current_user, db)

