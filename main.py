import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Function to create a pie chart
def plot_pie_chart(data, labels, title):
    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title(title)
    return fig

# Function to calculate totals based on portions
def calculate_totals(selected_data, portions):
    selected_data = selected_data.copy()
    selected_data["Portions"] = portions
    for column in ["Calories", "Total Fat (g)", "Protein (g)", "Carbs (g)", "Fiber (g)"]:
        selected_data[column] *= selected_data["Portions"]
    return selected_data, selected_data[["Calories", "Total Fat (g)", "Protein (g)", "Carbs (g)", "Fiber (g)"]].sum()

# Updated Bentley Dining Hall Data with additional nutrients
dining_hall_data = {
    "Monday": {
        "Breakfast": pd.DataFrame([
            {"Meal": "Bacon, Egg And Cheese Muffin", "Calories": 350, "Total Fat (g)": 12, "Protein (g)": 15, "Carbs (g)": 30, "Fiber (g)": 2},
            {"Meal": "Fried Egg O'muffin Sandwich", "Calories": 310, "Total Fat (g)": 10, "Protein (g)": 13, "Carbs (g)": 28, "Fiber (g)": 2},
            {"Meal": "Scrambled Eggs", "Calories": 190, "Total Fat (g)": 5, "Protein (g)": 12, "Carbs (g)": 2, "Fiber (g)": 0},
        ]),
        "Lunch": pd.DataFrame([
            {"Meal": "Rosemary Grilled Pork Chop", "Calories": 300, "Total Fat (g)": 10, "Protein (g)": 30, "Carbs (g)": 0, "Fiber (g)": 0},
            {"Meal": "Cheese Pizza", "Calories": 250, "Total Fat (g)": 8, "Protein (g)": 10, "Carbs (g)": 32, "Fiber (g)": 2},
        ]),
        "Dinner": pd.DataFrame([
            {"Meal": "Roast Loin Of Pork", "Calories": 210, "Total Fat (g)": 10, "Protein (g)": 25, "Carbs (g)": 0, "Fiber (g)": 0},
            {"Meal": "Rice & Red Beans", "Calories": 180, "Total Fat (g)": 3, "Protein (g)": 5, "Carbs (g)": 35, "Fiber (g)": 4},
        ]),
    },
    "Tuesday": {
        "Breakfast": pd.DataFrame([
            {"Meal": "Scrambled Eggs", "Calories": 190, "Total Fat (g)": 5, "Protein (g)": 12, "Carbs (g)": 2, "Fiber (g)": 0},
            {"Meal": "Oatmeal", "Calories": 110, "Total Fat (g)": 1, "Protein (g)": 4, "Carbs (g)": 20, "Fiber (g)": 3},
        ]),
        "Lunch": pd.DataFrame([
            {"Meal": "Beef Bulgogi Rice Bowl", "Calories": 470, "Total Fat (g)": 20, "Protein (g)": 35, "Carbs (g)": 50, "Fiber (g)": 5},
        ]),
        "Dinner": pd.DataFrame([
            {"Meal": "Pepperoni Pizza", "Calories": 250, "Total Fat (g)": 10, "Protein (g)": 10, "Carbs (g)": 32, "Fiber (g)": 2},
        ]),
    },
    "Wednesday": {
        "Breakfast": pd.DataFrame([
            {"Meal": "Egg And Cheese Breakfast Taco", "Calories": 210, "Total Fat (g)": 8, "Protein (g)": 10, "Carbs (g)": 22, "Fiber (g)": 2},
            {"Meal": "Blueberry Pancakes", "Calories": 220, "Total Fat (g)": 7, "Protein (g)": 5, "Carbs (g)": 32, "Fiber (g)": 1},
            {"Meal": "Scrambled Eggs", "Calories": 190, "Total Fat (g)": 5, "Protein (g)": 12, "Carbs (g)": 2, "Fiber (g)": 0},
        ]),
        "Lunch": pd.DataFrame([
            {"Meal": "Grilled Steak", "Calories": 260, "Total Fat (g)": 15, "Protein (g)": 25, "Carbs (g)": 0, "Fiber (g)": 0},
            {"Meal": "Fajita Chicken, Pintos And Rice Bowl", "Calories": 910, "Total Fat (g)": 35, "Protein (g)": 45, "Carbs (g)": 90, "Fiber (g)": 7},
        ]),
        "Dinner": pd.DataFrame([
            {"Meal": "Herb Roast Chicken Breast", "Calories": 130, "Total Fat (g)": 5, "Protein (g)": 25, "Carbs (g)": 0, "Fiber (g)": 0},
            {"Meal": "Chicken Nuggets", "Calories": 350, "Total Fat (g)": 20, "Protein (g)": 15, "Carbs (g)": 22, "Fiber (g)": 2},
        ]),
    },
}

# Sidebar for user personal info
st.sidebar.header("Personal Information")
weight = st.sidebar.number_input("Weight (kg):", min_value=30, max_value=200, value=70)
height = st.sidebar.number_input("Height (cm):", min_value=100, max_value=250, value=170)
age = st.sidebar.number_input("Age (years):", min_value=10, max_value=100, value=25)
gender = st.sidebar.selectbox("Gender:", ["Male", "Female", "Other"])
activity_level = st.sidebar.selectbox("Activity Level:", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])

# Calculate daily caloric needs
if gender == "Male":
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
else:
    bmr = 10 * weight + 6.25 * height - 5 * age - 161

activity_multiplier = {
    "Sedentary": 1.2,
    "Lightly Active": 1.375,
    "Moderately Active": 1.55,
    "Very Active": 1.725,
}
daily_caloric_needs = int(bmr * activity_multiplier[activity_level])
st.sidebar.metric("Recommended Daily Calories", f"{daily_caloric_needs} kcal")

# Sidebar for day and meal type selection
st.sidebar.header("Select Day and Meal Type")
selected_day = st.sidebar.selectbox("Select a Day:", list(dining_hall_data.keys()))
selected_meal_type = st.sidebar.selectbox("Select a Meal Type:", ["Breakfast", "Lunch", "Dinner"])

# Retrieve menu for selected day and meal type
menu_df = dining_hall_data[selected_day][selected_meal_type]
st.subheader(f"{selected_day} {selected_meal_type} Menu")
st.dataframe(menu_df)

# Allow users to select meals and portions
selected_meals = st.multiselect(
    "Select meals to add to your plan:",
    options=menu_df["Meal"].tolist()
)

if selected_meals:
    selected_data = menu_df[menu_df["Meal"].isin(selected_meals)]
    st.write("### Selected Meals")

    # Input portions for selected meals
    portions = []
    for meal in selected_meals:
        portions.append(st.number_input(f"Portions of {meal}:", min_value=1, max_value=10, value=1))

    # Calculate totals
    selected_data, totals = calculate_totals(selected_data, portions)

    # Display selected meals with portions
    st.table(selected_data)

    # Display summary
    st.write("### Summary")
    st.metric("Total Calories", f"{totals['Calories']} kcal")
    st.metric("Total Fat", f"{totals['Total Fat (g)']} g")
    st.metric("Total Protein", f"{totals['Protein (g)']} g")
    st.metric("Total Carbs", f"{totals['Carbs (g)']} g")
    st.metric("Total Fiber", f"{totals['Fiber (g)']} g")

    # Nutritional Breakdown Pie Chart
    st.subheader("Nutritional Breakdown")
    pie_chart = plot_pie_chart(
        data=[totals["Carbs (g)"], totals["Protein (g)"], totals["Total Fat (g)"]],
        labels=["Carbs (g)", "Protein (g)", "Total Fat (g)"],
        title="Nutritional Distribution"
    )
    st.pyplot(pie_chart)

    # Recommendations
    if totals["Calories"] > daily_caloric_needs:
        st.error("Your
