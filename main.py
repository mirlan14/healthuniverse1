pip install streamlit
import streamlit as st

st.title("AI-Driven Nutrition Planner")
st.sidebar.header("User Details")

age = st.sidebar.number_input("Enter your age:", min_value=1, max_value=120, step=1)
gender = st.sidebar.selectbox("Select your gender:", ["Male", "Female", "Other"])
allergies = st.sidebar.text_input("List your allergies (comma-separated):")
chronic_conditions = st.sidebar.multiselect(
    "Select chronic conditions:",
    ["Diabetes", "Hypertension", "Obesity"]
)

st.header("Personalized Meal Plan")
meals = ["Breakfast: Oatmeal with berries", 
         "Lunch: Grilled chicken salad", 
         "Dinner: Salmon with quinoa"]

for meal in meals:
    st.write(meal)

st.header("Personalized Meal Plan")
meals = ["Breakfast: Oatmeal with berries", 
         "Lunch: Grilled chicken salad", 
         "Dinner: Salmon with quinoa"]

for meal in meals:
    st.write(meal)
