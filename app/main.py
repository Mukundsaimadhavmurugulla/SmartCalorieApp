# app/main.py
from fastapi import FastAPI
#from sqlalchemy.orm import Session
from . import models, database

# 1. Create the database tables automatically
models.Base.metadata.create_all(bind=database.engine)

# 2. Start the App
app = FastAPI()

# 3. Dependency (How we get a database session)
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 4. A simple test route
@app.get("/")
def read_root():
    return {"message": "Welcome to Mukund's Calorie Tracker API!"}