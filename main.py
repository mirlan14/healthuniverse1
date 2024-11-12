import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Data for Breakfast, Lunch, and Dinner Menus
breakfast_data = {
    "Meal": [
        "Bacon, Egg And Cheese Muffin", "Fried Egg O’muffin Sandwich", "Scrambled Eggs", 
        "Bacon", "Fried Tater Tots", "Buttermilk Pancakes", "Everything Omelet", 
        "Grits", "Oatmeal", "Mango Banana Smoothie", "Strawberry Banana Smoothie", 
        "Pineapple & Honey Smoothie", "Mango Pineapple Smoothie", 
        "Brown Sugar Cinnamon Mini Scone", "Strawberry Shortcake Muffins", 
        "Scrambled Tofu", "Lyonnaise Potatoes", "Roasted Red Beets"
    ],
    "Calories": [350, 310, 190, 70, 250, 180, 290, 90, 110, 100, 100, 190, 110, 200, 130, 60, 45, 25],
    "Total Fat (g)": [12, 10, 5, 6, 15, 9, 11, 0.5, 1, 0.5, 0.3, 1.5, 0.3, 10, 8, 3, 1, 0.2],
    "Protein (g)": [15, 13, 12, 5, 2, 4, 10, 2, 3, 1, 2, 4, 1, 3, 4, 2, 1, 1],
}

lunch_data = {
    "Meal": [
        "Grilled Garlic Chicken", "Black Bean Burger", "Cheeseburger On Bun", 
        "French Fries", "Bbq Pork Riblet Sandwich", "Beef Bulgogi Rice Bowl", 
        "Cheese Pizza", "Vegetable Lovers Feast Pizza", "Pepperoni Pizza", 
        "Creamy Broccoli & Cheddar Soup", "Cilantro Cucumber Salad", 
        "Tabbouleh With Garbanzo Beans", "Salsa", "Cilantro Lime Brown Rice", 
        "Baja Roasted Vegetables"
    ],
    "Calories": [150, 240, 200, 150, 380, 470, 250, 290, 250, 200, 70, 110, 10, 120, 50],
    "Total Fat (g)": [2, 6, 10, 5, 15, 20, 8, 12, 10, 9, 1, 3, 0.2, 1, 0.5],
    "Protein (g)": [30, 10, 12, 2, 15, 35, 10, 8, 10, 6, 1, 3, 0.5, 2, 1],
}

dinner_data = {
    "Meal": [
        "Tomato, Bacon & Cheddar Baguette", "Beef Bulgogi Rice Bowl", 
        "Vegetable Lovers Feast Pizza", "Pepperoni Pizza", "Gluten-Free Penne", 
        "Simply Sauteed Broccoli Rabe", "Chili Con Carne", "Extra Firm Tofu", 
        "Baked Garlic Breadstick", "Latin Chipotle Quinoa Salad"
    ],
    "Calories": [540, 470, 290, 250, 170, 25, 190, 60, 90, 130],
    "Total Fat (g)": [20, 18, 12, 10, 5, 0.5, 7, 2, 3, 1],
    "Protein (g)": [25, 35, 10, 15, 6, 1, 15, 6, 2, 4],
}

# Convert data to DataFrames
breakfast_df = pd.DataFrame(breakfast_data)
lunch_df = pd.DataFrame(lunch_data)
dinner_df = pd.DataFrame(dinner_data)

# Function to calculate daily caloric needs (Mifflin-St Jeor Equation)
def calculate_calories(weight, height, age, gender, activity_level):
    if gender == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    activity_multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725
    }
    return bmr * activity_multipliers[activity_level]

# App Title
st.title("Personalized Nutrition and Meal Planning 🍴")

# Sidebar for Personal Information
st.sidebar.header("Personal Information")
weight = st.sidebar.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
height = st.sidebar.number_input("Height (cm)", min_value=100, max_value=250, value=170)
age = st.sidebar.number_input("Age (years)", min_value=10, max_value=100, value=25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
activity_level = st.sidebar.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])

# Calculate daily caloric needs
daily_caloric_needs = calculate_calories(weight, height, age, gender, activity_level)
st.sidebar.metric("Recommended Daily Calories", f"{int(daily_caloric_needs)} kcal")

# Meal Type Selection
st.sidebar.header("Choose a Meal Type")
meal_type = st.sidebar.selectbox("Select a Meal", ["Breakfast", "Lunch", "Dinner"])

# Select appropriate menu based on meal type
if meal_type == "Breakfast":
    menu_df = breakfast_df
elif meal_type == "Lunch":
    menu_df = lunch_df
else:
    menu_df = dinner_df

# Sidebar for Filtering
st.sidebar.header("Filter Your Options")
dietary_preference = st.sidebar.selectbox("Select a Dietary Option", ["All", "Vegan", "Vegetarian"])
calorie_limit = st.sidebar.slider("Set a Calorie Limit (per meal)", 50, 600, 300)

# Filter meals based on preferences
if dietary_preference != "All":
    filtered_menu = menu_df[(menu_df["Calories"] <= calorie_limit)]
else:
    filtered_menu = menu_df[menu_df["Calories"] <= calorie_limit]

# Display Menu
st.subheader(f"{meal_type} Menu")
st.dataframe(filtered_menu)

# Meal Planning and Recommendations
selected_meals = st.multiselect("Select meals to add to your plan:", options=filtered_menu["Meal"].tolist())
if selected_meals:
    selected_data = filtered_menu[filtered_menu["Meal"].isin(selected_meals)]
    total_calories = selected_data["Calories"].sum()

    # Display selected meals and summary
    st.write("### Selected Meals")
    st.table(selected_data)

    st.write("### Summary")
    st.metric("Total Calories", f"{total_calories} kcal")

    # Recommendations
    if total_calories > daily_caloric_needs:
        st.error("Your meal plan exceeds your daily caloric needs.")
    elif total_calories < daily_caloric_needs * 0.8:
        st.warning("Your meal plan is too low in calories.")
    else:
        st.success("Your meal plan is within your recommended caloric range.")

    # Nutritional Breakdown
    st.write("### Nutritional Breakdown")
    st.bar_chart(selected_data[["Calories", "Total Fat (g)", "Protein (g)"]])

# Footer
st.write("### Stay healthy and enjoy your meals! 🌟")
