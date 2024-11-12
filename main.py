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
    "Dietary Options": [
        "Contains Dairy, Egg, Vegetarian", "Contains Dairy, Egg, Vegetarian", "Contains Egg, Vegetarian",
        "Contains Meat", "Vegan", "Contains Dairy, Egg, Vegetarian", "Contains Dairy, Egg, Vegetarian",
        "Vegan", "Vegan", "Vegan", "Contains Dairy", "Vegetarian", "Contains Dairy",
        "Contains Dairy, Egg, Vegetarian", "Contains Dairy, Egg, Vegetarian",
        "Vegan", "Vegan", "Vegan"
    ]
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
    "Dietary Options": [
        "Contains Meat", "Vegan", "Contains Dairy, Gluten", "Vegan", "Contains Meat, Gluten", 
        "Contains Meat, Gluten", "Contains Dairy, Vegetarian", "Contains Dairy, Vegetarian", 
        "Contains Dairy, Meat", "Contains Dairy, Vegetarian", "Vegan", "Vegan", "Vegan", 
        "Vegan", "Vegan"
    ]
}

dinner_data = {
    "Meal": [
        "Tomato, Bacon & Cheddar Baguette", "Beef Bulgogi Rice Bowl", 
        "Vegetable Lovers Feast Pizza", "Pepperoni Pizza", "Gluten-Free Penne", 
        "Simply Sauteed Broccoli Rabe", "Chili Con Carne", "Extra Firm Tofu", 
        "Baked Garlic Breadstick", "Latin Chipotle Quinoa Salad"
    ],
    "Calories": [540, 470, 290, 250, 170, 25, 190, 60, 90, 130],
    "Dietary Options": [
        "Contains Dairy, Gluten, Meat", "Contains Meat, Gluten", 
        "Contains Dairy, Vegetarian", "Contains Dairy, Meat", "Vegan, Gluten-Free", 
        "Vegan", "Contains Meat", "Vegan", "Contains Gluten, Vegetarian", 
        "Vegan"
    ]
}

# Convert data to DataFrames
breakfast_df = pd.DataFrame(breakfast_data)
lunch_df = pd.DataFrame(lunch_data)
dinner_df = pd.DataFrame(dinner_data)

# App Title
st.title("Bentley University Dining Hall Nutrition and Meal Planner 🍴")

# Sidebar for meal selection
st.sidebar.header("Choose a Meal Type")
meal_type = st.sidebar.selectbox("Select a Meal", ["Breakfast", "Lunch", "Dinner"])

# Select the appropriate DataFrame based on meal type
if meal_type == "Breakfast":
    menu_df = breakfast_df
elif meal_type == "Lunch":
    menu_df = lunch_df
else:
    menu_df = dinner_df

# Sidebar for filtering dietary preferences and calorie limit
st.sidebar.header("Customize Your Preferences")
dietary_preference = st.sidebar.selectbox(
    "Select a Dietary Option",
    ["All", "Vegan", "Vegetarian", "Contains Dairy", "Contains Gluten", "Contains Meat"]
)
calorie_limit = st.sidebar.slider("Set a Calorie Limit (per meal)", 50, 600, 300)

# Filter menu based on preferences
if dietary_preference != "All":
    filtered_menu = menu_df[
        (menu_df["Dietary Options"].str.contains(dietary_preference)) & 
        (menu_df["Calories"] <= calorie_limit)
    ]
else:
    filtered_menu = menu_df[menu_df["Calories"] <= calorie_limit]

# Display dining hall menu
st.subheader(f"{meal_type} Menu")
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

    # Display meal plan and nutrition summary
    st.write("### Selected Meals")
    st.table(selected_data)

    st.write("### Nutrition Summary")
    st.metric("Total Calories", f"{total_calories} kcal")

    # Visualization: Calorie Distribution of Selected Meals
    st.subheader("Calorie Distribution of Selected Meals")
    fig, ax = plt.subplots()
    ax.bar(selected_data["Meal"], selected_data["Calories"], color='skyblue')
    ax.set_title("Calorie Distribution")
    ax.set_xlabel("Meal")
    ax.set_ylabel("Calories")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

# Footer
st.write("#### Stay healthy with delicious meals! 🌟")
