import streamlit as st
import pandas as pd
import numpy as np

# Simulated dining hall menu and nutrition data
menu_data = {
    "Meal": ["Grilled Chicken", "Vegetable Stir Fry", "Pasta Alfredo", "Garden Salad", "Beef Tacos"],
    "Calories": [250, 200, 400, 150, 350],
    "Protein (g)": [35, 10, 12, 5, 20],
    "Carbs (g)": [5, 30, 50, 10, 40],
    "Fat (g)": [5, 10, 20, 5, 15],
    "Dietary Options": ["High Protein", "Vegetarian", "Vegetarian", "Vegan", "High Protein"]
}
menu_df = pd.DataFrame(menu_data)

# App Title
st.title("University Dining Hall Nutrition and Meal Planner 🍴")

# Sidebar for user dietary preferences
st.sidebar.header("Customize Your Preferences")
dietary_preference = st.sidebar.selectbox(
    "Select a Dietary Option",
    ["All", "High Protein", "Vegetarian", "Vegan"]
)
calorie_limit = st.sidebar.slider("Set a Calorie Limit (per meal)", 100, 1000, 500)

# Filter menu based on preferences
if dietary_preference != "All":
    filtered_menu = menu_df[(menu_df["Dietary Options"] == dietary_preference) & 
                            (menu_df["Calories"] <= calorie_limit)]
else:
    filtered_menu = menu_df[menu_df["Calories"] <= calorie_limit]

# Display dining hall menu
st.subheader("Dining Hall Menu")
if filtered_menu.empty:
    st.warning("No meals available for the selected preferences. Please adjust your filters.")
else:
    st.dataframe(filtered_menu)

# Allow users to select meals for planning
st.subheader("Plan Your Meal")
selected_meals = st.multiselect(
    "Select meals to add to your plan:",
    options=filtered_menu["Meal"].tolist()
)

if selected_meals:
    # Calculate total nutrition for selected meals
    selected_data = menu_df[menu_df["Meal"].isin(selected_meals)]
    total_calories = selected_data["Calories"].sum()
    total_protein = selected_data["Protein (g)"].sum()
    total_carbs = selected_data["Carbs (g)"].sum()
    total_fat = selected_data["Fat (g)"].sum()

    # Display meal plan and nutrition summary
    st.write("### Selected Meals")
    st.table(selected_data)

    st.write("### Nutrition Summary")
    st.metric("Total Calories", f"{total_calories} kcal")
    st.metric("Total Protein", f"{total_protein} g")
    st.metric("Total Carbohydrates", f"{total_carbs} g")
    st.metric("Total Fat", f"{total_fat} g")

# Allow users to download their meal plan
if selected_meals:
    csv = selected_data.to_csv(index=False)
    st.download_button(
        label="Download Meal Plan as CSV",
        data=csv,
        file_name="meal_plan.csv",
        mime="text/csv"
    )

# Footer
st.write("#### Enjoy your meals while staying healthy! 🌟")
