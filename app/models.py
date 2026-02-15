# app/models.py
from sqlalchemy import Column, Integer, String, Float, Boolean
from .database import Base


class FoodItem(Base):
    __tablename__ = "food_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    # Macros per 100g
    calories = Column(Float)
    protein = Column(Float)
    carbs = Column(Float)
    fats = Column(Float)

    # The Extras you wanted
    fiber = Column(Float, default=0.0)
    sugar = Column(Float, default=0.0)
    is_ethnic = Column(Boolean, default=False)