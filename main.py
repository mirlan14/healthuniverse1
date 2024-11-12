import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Bentley University Dining Hall Menu Data
data = {
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
menu_df = pd.DataFrame(data)

# App Title
st.title("Bentley University Dining Hall Nutrition and Meal Planner 🍳")

# Sidebar for user dietary preferences
st.sidebar.header("Customize Your Preferences")
dietary_preference = st.sidebar.selectbox(
    "Select a Dietary Option",
    ["All", "Contains Dairy", "Contains Egg", "Vegetarian", "Vegan", "Contains Meat"]
)
calorie_limit = st.sidebar.slider("Set a Calorie Limit (per meal)", 50, 400, 300)

# Filter menu based on preferences
if dietary_preference != "All":
    filtered_menu = menu_df[
        (menu_df["Dietary Options"].str.contains(dietary_preference)) & 
        (menu_df["Calories"] <= calorie_limit)
    ]
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

# Visualization: Overall Calorie Distribution
st.subheader("Overall Calorie Distribution in Menu")
fig, ax = plt.subplots()
ax.hist(menu_df["Calories"], bins=10, color='lightgreen', edgecolor='black')
ax.set_title("Calorie Distribution")
ax.set_xlabel("Calories")
ax.set_ylabel("Frequency")
st.pyplot(fig)

# Visualization: Dietary Options Distribution
st.subheader("Dietary Options Distribution")
dietary_counts = menu_df["Dietary Options"].value_counts()
fig, ax = plt.subplots()
ax.pie(dietary_counts, labels=dietary_counts.index, autopct='%1.1f%%', startangle=140)
ax.set_title("Dietary Options")
st.pyplot(fig)

# Allow users to download their meal plan
if selected_meals:
    csv = selected_data.to_csv(index=False)
    st.download_button(
        label="Download Meal Plan as CSV",
        data=csv,
        file_name="bentley_meal_plan.csv",
        mime="text/csv"
    )

# Footer
st.write("#### Enjoy your breakfast while staying healthy at Bentley! 🥞")
