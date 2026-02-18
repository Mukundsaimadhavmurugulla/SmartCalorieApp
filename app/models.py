# app/models.py
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class FoodItem(Base):
    __tablename__ = "food_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    # Macros per 100g or per piece
    calories = Column(Float)
    protein = Column(Float)
    carbs = Column(Float)
    fats = Column(Float)

    fiber = Column(Float, default=0.0)
    sugar = Column(Float, default=0.0)
    is_ethnic = Column(Boolean, default=False)

    # Link to logs (Optional, but good practice)
    logs = relationship("DailyLog", back_populates="food")


class DailyLog(Base):
    __tablename__ = "daily_logs"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)  # Format: "YYYY-MM-DD"
    meal_type = Column(String)

    # How much did you eat?
    quantity_eaten = Column(Float)

    # Foreign Key (Links to the FoodItem table)
    food_id = Column(Integer, ForeignKey("food_items.id"))

    # Relationship (Lets us grab the food name easily)
    food = relationship("FoodItem", back_populates="logs")