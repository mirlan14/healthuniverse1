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
        {"Meal": "Bacon Slices", "Calories": 70, "Total Fat (g)": 6, "Protein (g)": 5, "Carbs (g)": 1, "Fiber (g)": 0},
        {"Meal": "Fried Tater Tots", "Calories": 250, "Total Fat (g)": 15, "Protein (g)": 2, "Carbs (g)": 22, "Fiber (g)": 2},
        {"Meal": "Buttermilk Pancakes", "Calories": 180, "Total Fat (g)": 9, "Protein (g)": 4, "Carbs (g)": 20, "Fiber (g)": 1},
        {"Meal": "Everything Omelet", "Calories": 290, "Total Fat (g)": 20, "Protein (g)": 18, "Carbs (g)": 3, "Fiber (g)": 0},
        {"Meal": "Grits", "Calories": 90, "Total Fat (g)": 1, "Protein (g)": 2, "Carbs (g)": 20, "Fiber (g)": 1},
        {"Meal": "Oatmeal", "Calories": 110, "Total Fat (g)": 2, "Protein (g)": 3, "Carbs (g)": 19, "Fiber (g)": 3},
        {"Meal": "Bacon", "Calories": 60, "Total Fat (g)": 5, "Protein (g)": 4, "Carbs (g)": 0, "Fiber (g)": 0},
        {"Meal": "Agave Roasted Peaches", "Calories": 20, "Total Fat (g)": 0, "Protein (g)": 0, "Carbs (g)": 5, "Fiber (g)": 1},
        {"Meal": "Roasted Mexican Potatoes", "Calories": 45, "Total Fat (g)": 1, "Protein (g)": 1, "Carbs (g)": 10, "Fiber (g)": 1},
        {"Meal": "Mango Banana Smoothie", "Calories": 100, "Total Fat (g)": 0, "Protein (g)": 1, "Carbs (g)": 24, "Fiber (g)": 1},
        {"Meal": "Strawberry Banana Smoothie", "Calories": 100, "Total Fat (g)": 0, "Protein (g)": 1, "Carbs (g)": 23, "Fiber (g)": 1},
        {"Meal": "Pineapple & Honey Smoothie", "Calories": 190, "Total Fat (g)": 0, "Protein (g)": 2, "Carbs (g)": 45, "Fiber (g)": 2},
        {"Meal": "Mango Pineapple Smoothie", "Calories": 110, "Total Fat (g)": 0, "Protein (g)": 1, "Carbs (g)": 26, "Fiber (g)": 1},
        {"Meal": "Brown Sugar Cinnamon Mini Scone", "Calories": 200, "Total Fat (g)": 10, "Protein (g)": 3, "Carbs (g)": 26, "Fiber (g)": 1},
        {"Meal": "Strawberry Shortcake Muffins", "Calories": 130, "Total Fat (g)": 5, "Protein (g)": 2, "Carbs (g)": 19, "Fiber (g)": 1},
        {"Meal": "Scrambled Tofu", "Calories": 60, "Total Fat (g)": 2, "Protein (g)": 7, "Carbs (g)": 1, "Fiber (g)": 1},
        {"Meal": "Lyonnaise Potatoes", "Calories": 45, "Total Fat (g)": 1, "Protein (g)": 1, "Carbs (g)": 10, "Fiber (g)": 1},
        {"Meal": "Roasted Red Beets", "Calories": 25, "Total Fat (g)": 0, "Protein (g)": 1, "Carbs (g)": 5, "Fiber (g)": 1},
    ]),
    },
   "Tuesday": {
    "Breakfast": pd.DataFrame([
        {"Meal": "Egg & Cheese Bagel With Sausage", "Calories": 500, "Total Fat (g)": 20, "Protein (g)": 22, "Carbs (g)": 55, "Fiber (g)": 3},
        {"Meal": "Scrambled Egg & Cheese On Bagel", "Calories": 300, "Total Fat (g)": 10, "Protein (g)": 15, "Carbs (g)": 35, "Fiber (g)": 2},
        {"Meal": "Scrambled Eggs", "Calories": 190, "Total Fat (g)": 5, "Protein (g)": 12, "Carbs (g)": 2, "Fiber (g)": 0},
        {"Meal": "Oven Roasted Greek Potatoes", "Calories": 100, "Total Fat (g)": 2, "Protein (g)": 2, "Carbs (g)": 20, "Fiber (g)": 2},
        {"Meal": "Grilled Kielbasa", "Calories": 190, "Total Fat (g)": 16, "Protein (g)": 8, "Carbs (g)": 1, "Fiber (g)": 0},
        {"Meal": "French Waffle", "Calories": 180, "Total Fat (g)": 7, "Protein (g)": 4, "Carbs (g)": 22, "Fiber (g)": 1},
        {"Meal": "Everything Omelet", "Calories": 290, "Total Fat (g)": 20, "Protein (g)": 18, "Carbs (g)": 3, "Fiber (g)": 0},
        {"Meal": "Grits", "Calories": 90, "Total Fat (g)": 1, "Protein (g)": 2, "Carbs (g)": 20, "Fiber (g)": 1},
        {"Meal": "Oatmeal", "Calories": 110, "Total Fat (g)": 2, "Protein (g)": 3, "Carbs (g)": 19, "Fiber (g)": 3},
        {"Meal": "Griddled Ham Steak", "Calories": 70, "Total Fat (g)": 3, "Protein (g)": 10, "Carbs (g)": 1, "Fiber (g)": 0},
        {"Meal": "Potato & Kale Hash", "Calories": 130, "Total Fat (g)": 5, "Protein (g)": 3, "Carbs (g)": 15, "Fiber (g)": 2},
        {"Meal": "Chocolate Strawberry Chia Seed Pudding", "Calories": 290, "Total Fat (g)": 15, "Protein (g)": 8, "Carbs (g)": 28, "Fiber (g)": 6},
        {"Meal": "Strawberry Banana Smoothie", "Calories": 100, "Total Fat (g)": 0, "Protein (g)": 1, "Carbs (g)": 23, "Fiber (g)": 1},
        {"Meal": "Mango Banana Smoothie", "Calories": 100, "Total Fat (g)": 0, "Protein (g)": 1, "Carbs (g)": 24, "Fiber (g)": 1},
        {"Meal": "Mango Pineapple Smoothie", "Calories": 110, "Total Fat (g)": 0, "Protein (g)": 1, "Carbs (g)": 26, "Fiber (g)": 1},
        {"Meal": "Fresh Melons, Strawberries & Grapes", "Calories": 25, "Total Fat (g)": 0, "Protein (g)": 0, "Carbs (g)": 6, "Fiber (g)": 0},
        {"Meal": "Scrambled Vegan Egg Substitute", "Calories": 100, "Total Fat (g)": 3, "Protein (g)": 8, "Carbs (g)": 2, "Fiber (g)": 1},
        {"Meal": "Shredded Hash Browns", "Calories": 260, "Total Fat (g)": 12, "Protein (g)": 3, "Carbs (g)": 30, "Fiber (g)": 2},
        {"Meal": "Roasted Carrots", "Calories": 40, "Total Fat (g)": 0, "Protein (g)": 1, "Carbs (g)": 10, "Fiber (g)": 3},
    ]),
    },
    "Wednesday": {
    "Breakfast": pd.DataFrame([
        {"Meal": "Ham, Egg And Cheese Taco", "Calories": 220, "Total Fat (g)": 12, "Protein (g)": 14, "Carbs (g)": 18, "Fiber (g)": 2},
        {"Meal": "Egg And Cheese Breakfast Taco", "Calories": 210, "Total Fat (g)": 10, "Protein (g)": 12, "Carbs (g)": 17, "Fiber (g)": 2},
        {"Meal": "Blueberry Pancakes", "Calories": 220, "Total Fat (g)": 7, "Protein (g)": 5, "Carbs (g)": 32, "Fiber (g)": 1},
        {"Meal": "O'Brien Potatoes", "Calories": 140, "Total Fat (g)": 5, "Protein (g)": 2, "Carbs (g)": 18, "Fiber (g)": 2},
        {"Meal": "Pork Sausage Link", "Calories": 100, "Total Fat (g)": 8, "Protein (g)": 5, "Carbs (g)": 1, "Fiber (g)": 0},
        {"Meal": "Scrambled Eggs", "Calories": 190, "Total Fat (g)": 5, "Protein (g)": 12, "Carbs (g)": 2, "Fiber (g)": 0},
        {"Meal": "Everything Omelet", "Calories": 290, "Total Fat (g)": 20, "Protein (g)": 18, "Carbs (g)": 3, "Fiber (g)": 0},
        {"Meal": "Grits", "Calories": 90, "Total Fat (g)": 1, "Protein (g)": 2, "Carbs (g)": 20, "Fiber (g)": 1},
        {"Meal": "Oatmeal", "Calories": 110, "Total Fat (g)": 2, "Protein (g)": 3, "Carbs (g)": 19, "Fiber (g)": 3},
        {"Meal": "Hash Browned Potatoes", "Calories": 120, "Total Fat (g)": 6, "Protein (g)": 2, "Carbs (g)": 15, "Fiber (g)": 2},
        {"Meal": "Turkey Sausage Patty", "Calories": 80, "Total Fat (g)": 6, "Protein (g)": 8, "Carbs (g)": 0, "Fiber (g)": 0},
        {"Meal": "Sweet Potato Pancakes", "Calories": 270, "Total Fat (g)": 8, "Protein (g)": 6, "Carbs (g)": 40, "Fiber (g)": 4},
        {"Meal": "Mango Banana Smoothie", "Calories": 100, "Total Fat (g)": 0, "Protein (g)": 1, "Carbs (g)": 24, "Fiber (g)": 1},
        {"Meal": "Mango Pineapple Smoothie", "Calories": 110, "Total Fat (g)": 0, "Protein (g)": 1, "Carbs (g)": 26, "Fiber (g)": 1},
        {"Meal": "Pineapple & Honey Smoothie", "Calories": 190, "Total Fat (g)": 0, "Protein (g)": 2, "Carbs (g)": 45, "Fiber (g)": 2},
        {"Meal": "Strawberry Banana Smoothie", "Calories": 100, "Total Fat (g)": 0, "Protein (g)": 1, "Carbs (g)": 23, "Fiber (g)": 1},
        {"Meal": "Sauteed Peppers & Onions", "Calories": 80, "Total Fat (g)": 5, "Protein (g)": 1, "Carbs (g)": 8, "Fiber (g)": 2},
        {"Meal": "Scrambled Tofu", "Calories": 60, "Total Fat (g)": 3, "Protein (g)": 6, "Carbs (g)": 2, "Fiber (g)": 1},
        {"Meal": "Classic Grits", "Calories": 100, "Total Fat (g)": 1, "Protein (g)": 2, "Carbs (g)": 22, "Fiber (g)": 1},
    ]),
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
    title="Nutritional Distribution")
    st.pyplot(pie_chart)

    # Recommendations
    if totals["Calories"] > daily_caloric_needs:
        st.error("Your meal plan exceeds your daily caloric needs. Consider reducing high-calorie items.")
    elif totals["Calories"] < daily_caloric_needs * 0.8:
        st.warning("Your meal plan is too low in calories. Consider adding more nutrient-dense meals.")
    else:
        st.success("Your meal plan is within your recommended caloric range. Keep it up!")
    
    # Dietitian Section
    st.markdown("---")
    st.header("Need Help with Your Diet?")
    st.write("If you have questions or concerns about your diet, you can book an appointment with our on-site campus dietitian.")
    
    # Display dietitian information
    st.image("images/Hayley_tcm17-45509.jpg", caption="Hayley Ruff RD, LDN", width=300)
    st.write("**Dietitian: Hayley Ruff RD, LDN**")
    st.write("📧 **Email:** [hayley.ruff@sodexo.com](mailto:hayley.ruff@sodexo.com)")
    st.write("📞 **Phone:** +1 (508) 414-9633")
    
    # Appointment Booking Form
    st.subheader("Book an Appointment")
    with st.form("dietitian_appointment_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("What would you like to discuss?")
        submitted = st.form_submit_button("Submit Appointment Request")
    
        if submitted:
            st.success(f"Thank you, {name}! Your request has been submitted. Hayley Ruff will reach out to you at {email} soon.")
