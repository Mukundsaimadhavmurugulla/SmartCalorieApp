import requests
import time

# The URL of your local API
API_URL = "http://127.0.0.1:8000/food/"

# --- THE MEGA INDIAN FOOD DATABASE ---
# Values are estimated for HOME-COOKED versions (less oil/butter than restaurants)

indian_foods = [
    # --- STAPLES (Rice & Breads) ---
    {"name": "White Rice (Cooked) (100g)", "calories": 130, "protein": 2.7, "carbs": 28, "fats": 0.3, "fiber": 0.4,
     "is_ethnic": True},
    {"name": "Brown Rice (Cooked) (100g)", "calories": 111, "protein": 2.6, "carbs": 23, "fats": 0.9, "fiber": 1.8,
     "is_ethnic": True},
    {"name": "Chapati / Phulka (1 piece)", "calories": 104, "protein": 3, "carbs": 18, "fats": 3, "fiber": 2.5,
     "is_ethnic": True},
    {"name": "Paratha (Plain/Oil) (1 piece)", "calories": 180, "protein": 4, "carbs": 25, "fats": 8, "fiber": 3,
     "is_ethnic": True},
    {"name": "Aloo Paratha (1 piece)", "calories": 210, "protein": 5, "carbs": 30, "fats": 9, "fiber": 3,
     "is_ethnic": True},
    {"name": "Curd / Dahi (100g)", "calories": 60, "protein": 3.5, "carbs": 4.7, "fats": 3.3, "fiber": 0,
     "is_ethnic": True},

    # --- BREAKFAST HEROES ---
    {"name": "Idli (1 piece)", "calories": 39, "protein": 2, "carbs": 8, "fats": 0.2, "fiber": 0.5, "is_ethnic": True},
    {"name": "Dosa (Plain/Home) (1 piece)", "calories": 133, "protein": 4, "carbs": 22, "fats": 3, "fiber": 0.5,
     "is_ethnic": True},
    {"name": "Masala Dosa (1 piece)", "calories": 350, "protein": 6, "carbs": 45, "fats": 15, "fiber": 2,
     "is_ethnic": True},
    {"name": "Poha (Potato/Onion) (100g)", "calories": 130, "protein": 2.5, "carbs": 23, "fats": 4, "fiber": 1,
     "is_ethnic": True},
    {"name": "Upma (Rava) (100g)", "calories": 140, "protein": 3, "carbs": 22, "fats": 5, "fiber": 1,
     "is_ethnic": True},
    {"name": "Oats (Cooked with Water) (100g)", "calories": 70, "protein": 2.5, "carbs": 12, "fats": 1.4, "fiber": 2,
     "is_ethnic": False},

    # --- DALS & LENTILS (The Protein Source) ---
    {"name": "Dal Tadka (Yellow) (100g)", "calories": 110, "protein": 6, "carbs": 12, "fats": 4, "fiber": 3,
     "is_ethnic": True},
    {"name": "Dal Fry (Restaurant Style) (100g)", "calories": 150, "protein": 6, "carbs": 14, "fats": 8, "fiber": 3,
     "is_ethnic": True},
    {"name": "Sambar (with Veggies) (100g)", "calories": 85, "protein": 4, "carbs": 12, "fats": 2, "fiber": 3,
     "is_ethnic": True},
    {"name": "Rasam (Tomato/Pepper) (100g)", "calories": 40, "protein": 1, "carbs": 6, "fats": 1, "fiber": 0.5,
     "is_ethnic": True},
    {"name": "Chana Masala (Chickpeas) (100g)", "calories": 160, "protein": 7, "carbs": 20, "fats": 6, "fiber": 6,
     "is_ethnic": True},
    {"name": "Rajma (Red Kidney Beans) (100g)", "calories": 140, "protein": 6, "carbs": 18, "fats": 5, "fiber": 5,
     "is_ethnic": True},

    # --- VEGETABLE CURRIES (Sabzi) ---
    {"name": "Aloo Gobi (Dry) (100g)", "calories": 110, "protein": 3, "carbs": 14, "fats": 5, "fiber": 3,
     "is_ethnic": True},
    {"name": "Bhindi Fry (Okra) (100g)", "calories": 130, "protein": 3, "carbs": 9, "fats": 8, "fiber": 4,
     "is_ethnic": True},
    {"name": "Palak Paneer (Home Style) (100g)", "calories": 180, "protein": 9, "carbs": 6, "fats": 14, "fiber": 2,
     "is_ethnic": True},
    {"name": "Paneer Butter Masala (100g)", "calories": 250, "protein": 10, "carbs": 8, "fats": 20, "fiber": 1,
     "is_ethnic": True},
    {"name": "Mix Veg Curry (100g)", "calories": 100, "protein": 2, "carbs": 10, "fats": 6, "fiber": 3,
     "is_ethnic": True},
    {"name": "Baingan Bharta (Eggplant) (100g)", "calories": 90, "protein": 2, "carbs": 10, "fats": 5, "fiber": 4,
     "is_ethnic": True},
    {"name": "Cabbage Poriyal/Sabzi (100g)", "calories": 80, "protein": 2, "carbs": 9, "fats": 4, "fiber": 3,
     "is_ethnic": True},

    # --- NON-VEG (Home Style) ---
    {"name": "Chicken Curry (Home Style) (100g)", "calories": 140, "protein": 16, "carbs": 3, "fats": 7, "fiber": 0,
     "is_ethnic": True},
    {"name": "Chicken Biryani (Home) (100g)", "calories": 170, "protein": 9, "carbs": 20, "fats": 6, "fiber": 1,
     "is_ethnic": True},
    {"name": "Egg Curry (100g)", "calories": 130, "protein": 9, "carbs": 4, "fats": 9, "fiber": 0, "is_ethnic": True},
    {"name": "Fish Fry (Shallow Fried) (1 piece)", "calories": 180, "protein": 18, "carbs": 2, "fats": 10, "fiber": 0,
     "is_ethnic": True},
    {"name": "Grilled Chicken Breast (100g)", "calories": 165, "protein": 31, "carbs": 0, "fats": 3.6, "fiber": 0,
     "is_ethnic": False},

    # --- SNACKS & EXTRAS ---
    {"name": "Samosa (1 piece)", "calories": 260, "protein": 4, "carbs": 24, "fats": 17, "fiber": 2, "is_ethnic": True},
    {"name": "Chai / Tea (with Milk/Sugar) (1 cup)", "calories": 80, "protein": 2, "carbs": 10, "fats": 3, "fiber": 0,
     "is_ethnic": True},
    {"name": "Coffee (Instant with Milk) (1 cup)", "calories": 90, "protein": 3, "carbs": 10, "fats": 3, "fiber": 0,
     "is_ethnic": False},
    {"name": "Hard Boiled Egg (1 piece)", "calories": 70, "protein": 6, "carbs": 0.6, "fats": 5, "fiber": 0,
     "is_ethnic": False},

    # --- FRUITS ---
    {"name": "Banana (1 piece)", "calories": 105, "protein": 1.3, "carbs": 27, "fats": 0.4, "fiber": 3,
     "is_ethnic": False},
    {"name": "Apple (1 piece)", "calories": 95, "protein": 0.5, "carbs": 25, "fats": 0.3, "fiber": 4.4,
     "is_ethnic": False},
    {"name": "Watermelon (100g)", "calories": 30, "protein": 0.6, "carbs": 8, "fats": 0.2, "fiber": 0.4,
     "is_ethnic": False},
    {"name": "Muskmelon (100g)", "calories": 34, "protein": 0.8, "carbs": 8, "fats": 0.2, "fiber": 0.9,
     "is_ethnic": False}
]

print(f"🚀 Starting Mega-Batch Upload of {len(indian_foods)} Items...")

# A small counter to see progress
count = 0

for food in indian_foods:
    try:
        # We add a small delay so we don't overwhelm your local server instantly
        time.sleep(0.05)

        response = requests.post(API_URL, json=food)
        if response.status_code == 200:
            print(f"✅ [{count + 1}] Added: {food['name']}")
            count += 1
        else:
            print(f"❌ Failed: {food['name']}")
    except Exception as e:
        print(f"Error connecting to server: {e}")

print("✨ BOOM! Your database is now populated with 40+ Indian Dishes.")
print("✨ Restart your Streamlit Dashboard to see them!")