import streamlit as st
import requests
import pandas as pd

# --- CONFIGURATION ---
API_URL = "http://127.0.0.1:8000"
st.set_page_config(page_title="SmartCalorie", page_icon="🥗", layout="wide")

# --- SIDEBAR: USER GOALS ---
st.sidebar.title("👤 Mukund's Goals")
# Hardcoded for now, but we can make these editable later
GOAL_CALORIES = 2400
GOAL_PROTEIN = 160

st.sidebar.divider()

# --- MAIN APP ---
st.title("🥗 SmartCalorie Tracker")

# 1. FETCH DATA (The Pantry)
try:
    response = requests.get(f"{API_URL}/food/")
    food_list = response.json() if response.status_code == 200 else []
except:
    st.error("⚠️ Backend is offline. Run 'uvicorn app.main:app --reload'")
    food_list = []

# --- LOGGING SECTION ---
if food_list:
    st.subheader("🍽️ Log Your Meal")

    food_names = sorted([item['name'] for item in food_list])
    selected_name = st.selectbox("Search for a dish...", food_names)

    food_item = next((f for f in food_list if f['name'] == selected_name), None)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        # SMART UNIT LOGIC 🧠
        if "(100g)" in selected_name:
            st.info("⚖️ Measured by Weight")
            quantity = st.number_input("How many Grams?", min_value=10, max_value=1000, value=150, step=10)
            multiplier = quantity / 100.0  # Convert 150g -> 1.5 units
        else:
            st.info("🔢 Measured by Count")
            quantity = st.number_input("How many Pieces/Servings?", min_value=0.5, max_value=20.0, value=1.0, step=0.5)
            multiplier = quantity

    total_cal = food_item['calories'] * multiplier
    total_prot = food_item['protein'] * multiplier

    with col2:
        st.metric("Calories", f"{total_cal:.0f} kcal")
    with col3:
        st.metric("Protein", f"{total_prot:.1f} g")

    # THE SAVE BUTTON (Now writes to DB!)
    if st.button("Add to Daily Log ➕", type="primary"):
        log_data = {
            "food_name": selected_name,
            "quantity": multiplier,  # We send the raw multiplier (e.g. 1.5)
            "calories_eaten": total_cal,
            "protein_eaten": total_prot
        }

        # Send to API
        res = requests.post(f"{API_URL}/log/", json=log_data)

        if res.status_code == 200:
            st.success(f"Saved {selected_name} to database!")
            st.rerun()  # Refresh page to show new data
        else:
            st.error("Failed to save log.")

# --- TODAY'S HISTORY (Fetch from DB) ---
st.divider()
st.subheader("📊 Today's Progress")

# Fetch Today's Log from API
try:
    log_res = requests.get(f"{API_URL}/log/today")
    today_data = log_res.json() if log_res.status_code == 200 else []
except:
    today_data = []

if today_data:
    df = pd.DataFrame(today_data)
    st.dataframe(df, use_container_width=True)

    total_cals_eaten = df["Calories"].sum()
    total_prot_eaten = df["Protein"].sum()

    # Progress Bars
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Calories Eaten", f"{total_cals_eaten:.0f} / {GOAL_CALORIES}")
        st.progress(min(total_cals_eaten / GOAL_CALORIES, 1.0))
    with c2:
        st.metric("Protein Eaten", f"{total_prot_eaten:.1f}g / {GOAL_PROTEIN}g")
        st.progress(min(total_prot_eaten / GOAL_PROTEIN, 1.0))
else:
    st.info("No meals logged yet today.")