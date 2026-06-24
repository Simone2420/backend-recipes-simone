from config.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    #relations
    recipes = relationship("RecipeIngredient", back_populates="ingredient", cascade="all, delete")
    images = relationship("IngredientImage", back_populates="ingredient", cascade="all, delete")


class IngredientImage(Base):
    __tablename__ = "ingredient_images"
    id = Column(Integer, primary_key=True, index=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))
    image_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    #relations
    ingredient = relationship("Ingredient", back_populates="images")

class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))
    quantity = Column(String(255))
    measurement_unit = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    #relations
    recipe = relationship("Recipe", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="recipes")

    @property
    def name(self) -> str:
        """Expone el nombre del ingrediente para que el schema Pydantic pueda leerlo."""
        return self.ingredient.name if self.ingredient else None

    @property
    def images(self) -> list:
        """Expone las imágenes del ingrediente para que el schema Pydantic pueda leerlas."""
        return self.ingredient.images if self.ingredient else []