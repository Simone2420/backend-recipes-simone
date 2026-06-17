from datetime import datetime
from config.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    difficulty_id = Column(Integer, ForeignKey("difficulties.id"))
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_active = Column(Boolean, default=True)
    #relations
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="recipes")
    difficulty = relationship("Difficulty", back_populates="recipes")
    comments = relationship("Comment", back_populates="recipe")
    ingredient = relationship("Ingredient", secondary="recipe_ingredients", back_populates="recipes")
    recipe_image = relationship("RecipeImage", back_populates="recipe")
    recipe_rating = relationship("RecipeRating", back_populates="recipe")
    
class Difficulty(Base):
    __tablename__ = "difficulties"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    #relations
    recipes = relationship("Recipe", back_populates="difficulties")
    
class RecipeInfo(Base):
    __tablename__ = "recipe_infos"
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    prep_time = Column(Integer)
    cook_time = Column(Integer)
    total_time = Column(Integer)
    calories = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    #relations
    recipe = relationship("Recipe", back_populates="infos")
    
class RecipeRating(Base):
    __tablename__ = "recipe_ratings"
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    #relations
    recipe = relationship("Recipe", back_populates="ratings")
    user = relationship("User", back_populates="ratings")

class RecipeImage(Base):
    __tablename__ = "recipe_images"
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    image_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    #relations
    recipe = relationship("Recipe", back_populates="images")