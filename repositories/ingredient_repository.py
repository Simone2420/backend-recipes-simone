from sqlalchemy.orm import Session
from models.ingredients import Ingredient, IngredientImage
from schemas.ingredients import IngredientCreate, IngredientUpdate

class IngredientRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def get_ingredient_by_id(self, ingredient_id: int) -> Ingredient:
        return self.db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
        
    def get_ingredient_by_name(self, name: str) -> Ingredient:
        return self.db.query(Ingredient).filter(Ingredient.name.ilike(name)).first()
        
    def get_all_ingredients(self, skip: int = 0, limit: int = 100) -> list[Ingredient]:
        return self.db.query(Ingredient).offset(skip).limit(limit).all()
        
    def create_ingredient(self, ingredient: IngredientCreate) -> Ingredient:
        db_ingredient = Ingredient(name=ingredient.name)
        self.db.add(db_ingredient)
        self.db.commit()
        self.db.refresh(db_ingredient)
        return db_ingredient
        
    def update_ingredient(self, db_ingredient: Ingredient, ingredient_update: IngredientUpdate) -> Ingredient:
        update_data = ingredient_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_ingredient, key, value)
        self.db.commit()
        self.db.refresh(db_ingredient)
        return db_ingredient

    def add_ingredient_image(self, ingredient_id: int, image_url: str) -> IngredientImage:
        db_img = IngredientImage(ingredient_id=ingredient_id, image_url=image_url)
        self.db.add(db_img)
        self.db.commit()
        self.db.refresh(db_img)
        return db_img
