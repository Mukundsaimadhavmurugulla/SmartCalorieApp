# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date
#from typing import List

from . import models, database

# 1. Initialize Database
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


# 2. Database Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- SCHEMAS (Inputs) ---
class FoodCreate(BaseModel):
    name: str
    calories: float
    protein: float
    carbs: float
    fats: float
    fiber: float = 0.0
    sugar: float = 0.0
    is_ethnic: bool = False


class LogCreate(BaseModel):
    food_name: str
    quantity: float
    calories_eaten: float
    protein_eaten: float


# --- ROUTES ---

@app.post("/food/")
def create_food(food: FoodCreate, db: Session = Depends(get_db)):
    # FIXED: Used model_dump() instead of dict() for Pydantic V2
    db_food = models.FoodItem(**food.model_dump())
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food


@app.get("/food/")
def read_foods(db: Session = Depends(get_db)):
    return db.query(models.FoodItem).all()


@app.post("/log/")
def log_meal(log: LogCreate, db: Session = Depends(get_db)):
    today = date.today().isoformat()

    # Find the food ID based on the name sent from the dashboard
    food_item = db.query(models.FoodItem).filter(models.FoodItem.name == log.food_name).first()

    if not food_item:
        raise HTTPException(status_code=404, detail="Food not found")

    # Create the log entry
    db_log = models.DailyLog(
        date=today,
        meal_type="Any",
        food_id=food_item.id,
        quantity_eaten=log.quantity
    )

    db.add(db_log)
    db.commit()
    return {"status": "Logged", "food": log.food_name}


@app.get("/log/today")
def get_today_log(db: Session = Depends(get_db)):
    today = date.today().isoformat()

    # Get all logs for today
    logs = db.query(models.DailyLog).filter(models.DailyLog.date == today).all()

    output = []
    for log in logs:
        if log.food:
            multiplier = log.quantity_eaten

            # Smart Unit Detection for Display
            if "(100g)" in log.food.name:
                qty_display = f"{int(multiplier * 100)}g"
            else:
                qty_display = f"{multiplier} pcs"

            output.append({
                "Food": log.food.name,
                "Qty": qty_display,
                # Recalculate based on the stored multiplier
                "Calories": log.food.calories * multiplier,
                "Protein": log.food.protein * multiplier
            })

    return output