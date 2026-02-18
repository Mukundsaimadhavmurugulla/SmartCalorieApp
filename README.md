# Smart Calorie App & Nutrition Analyzer 🥗

A backend application built to solve the difficulty of tracking calories for home-cooked and ethnic foods. This project demonstrates professional backend architecture using Python, SQL, and REST API principles.

## 🚀 Key Features
- **Smart Tracking:** Logs complex nutritional data including Fiber, Sugar, and Macros.
- **Ethnic Food Logic:** Custom algorithm (`is_ethnic` flag) to estimate calories for non-standard homemade recipes.
- **Health Analytics:** SQL-powered filtering to identify "High Protein" or "Low Sugar" options.
- **Data Integrity:** Strict validation using Pydantic models to prevent bad data entry.

## 🛠️ Technical Stack
- **Language:** Python 3.9+
- **Framework:** FastAPI (for high-performance API endpoints)
- **Database:** SQLAlchemy ORM & SQLite (Relational Database Design)
- **Tools:** Git, Pydantic, Uvicorn

## 📂 Project Structure
- `main.py` - The entry point for the API and routing logic.
- `models.py` - SQLAlchemy database models (The "Blueprint").
- `database.py` - Database connection handling.
