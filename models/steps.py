from config.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class Step(Base):
    __tablename__ = "steps"
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    content = Column(String(255))
    description = Column(String(500))
    order = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    #relations
    recipe = relationship("Recipe", back_populates="steps")

class StepImage(Base):
    __tablename__ = "step_images"
    id = Column(Integer, primary_key=True, index=True)
    step_id = Column(Integer, ForeignKey("steps.id"))
    image_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    #relations
    step = relationship("Step", back_populates="images")


# class StepVideo(Base):
#     __tablename__ = "step_videos"
#     id = Column(Integer, primary_key=True, index=True)
#     step_id = Column(Integer, ForeignKey("steps.id"))
#     video_url = Column(String(255))
#     created_at = Column(DateTime, default=datetime.now)
#     updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
#     #relations
#     step = relationship("Step", back_populates="videos")