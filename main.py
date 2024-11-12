import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    for column in ["Calories", "Total Fat (g)", "Protein (g)"]:
        selected_data[column] *= selected_data["Portions"]
    return selected_data, selected_data[["Calories", "Total Fat (g)", "Protein (g)"]].sum()

# Additional features: Meal Recommendations and Nutritional Insights
def provide_recommendations(total_calories, daily_needs):
    if total_calories > daily_needs:
        return "Your meal plan exceeds your daily caloric needs. Consider reducing portion sizes or choosing lower-calorie options."
    elif total_calories < daily_needs * 0.8:
        return "Your meal plan is too low in calories. Add more nutritious options to meet your energy requirements."
    else:
        return "Your meal plan is within the recommended caloric range. Keep it up!"

# Function to display daily nutritional goals comparison
def plot_goals_comparison(totals, daily_goals):
    fig, ax = plt.subplots()
    nutrients = totals.index.tolist()
    values = totals.values
    goals = [daily_goals.get(nutrient, 0) for nutrient in nutrients]
    ax.bar(nutrients, values, label="Your Intake", alpha=0.7)
    ax.bar(nutrients, goals, label="Recommended Goals", alpha=0.5)
    ax.set_title("Comparison of Intake vs Goals")
    ax.set_ylabel("Amount")
    ax.legend()
    return fig

# Sample Data for Monday and Tuesday Menus
menus = {
    "Monday": {
        "Breakfast": pd.DataFrame([
            {"Meal": "Bacon, Egg And Cheese Muffin", "Calories": 350, "Total Fat (g)": 12, "Protein (g)": 15},
            {"Meal": "Fried Egg O’muffin Sandwich", "Calories": 310, "Total Fat (g)": 10, "Protein (g)": 13},
            {"Meal": "Scrambled Eggs", "Calories": 190, "Total Fat (g)": 5, "Protein (g)": 12},
        ]),
        "Lunch": pd.DataFrame([
            {"Meal": "Beef Bulgogi Rice Bowl", "Calories": 470, "Total Fat (g)": 20, "Protein (g)": 35},
            {"Meal": "Cheese Pizza", "Calories": 250, "Total Fat (g)": 8, "Protein (g)": 10},
        ]),
        "Dinner": pd.DataFrame([
            {"Meal": "Pepperoni Pizza", "Calories": 250, "Total Fat (g)": 10, "Protein (g)": 10},
            {"Meal": "Grilled Garlic Chicken", "Calories": 150, "Total Fat (g)": 2, "Protein (g)": 30},
        ]),
    },
    "Tuesday": {
        "Breakfast": pd.DataFrame([
            {"Meal": "Egg & Cheese Bagel With Sausage", "Calories": 500, "Total Fat (g)": 18, "Protein (g)": 20},
            {"Meal": "Scrambled Egg & Cheese On Bagel", "Calories": 300, "Total Fat (g)": 10, "Protein (g)": 15},
            {"Meal": "French Waffle", "Calories": 180, "Total Fat (g)": 7, "Protein (g)": 5},
        ]),
        "Lunch": pd.DataFrame([
            {"Meal": "Steamed Italian Vegetable Medley", "Calories": 45, "Total Fat (g)": 0.5, "Protein (g)": 1},
            {"Meal": "Rosemary Grilled Pork Chop", "Calories": 300, "Total Fat (g)": 10, "Protein (g)": 30},
        ]),
        "Dinner": pd.DataFrame([
            {"Meal": "Tuna Cheddar Melt", "Calories": 520, "Total Fat (g)": 18, "Protein (g)": 25},
            {"Meal": "Simply Grilled Fresh Cod", "Calories": 150, "Total Fat (g)": 2, "Protein (g)": 30},
        ]),
    },
}

# Sidebar to select day and meal type
st.sidebar.header("Select Day and Meal")
selected_day = st.sidebar.selectbox("Select a Day:", list(menus.keys()))
selected_meal_type = st.sidebar.selectbox("Select a Meal Type:", ["Breakfast", "Lunch", "Dinner"])

# Retrieve menu for selected day and meal type
menu_df = menus[selected_day][selected_meal_type]

# Display menu
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

    # Nutritional Breakdown Pie Chart
    st.subheader("Nutritional Breakdown")
    pie_chart = plot_pie_chart(
        data=totals.values,
        labels=totals.index,
        title="Nutritional Distribution"
    )
    st.pyplot(pie_chart)

    # Recommendations
    daily_caloric_needs = 2000  # Example value for demonstration
    st.write(provide_recommendations(totals["Calories"], daily_caloric_needs))

    # Daily Goals Comparison
    daily_goals = {"Calories": 2000, "Total Fat (g)": 70, "Protein (g)": 50}  # Example goals
    st.subheader("Comparison with Recommended Daily Goals")
    comparison_chart = plot_goals_comparison(totals, daily_goals)
    st.pyplot(comparison_chart)

# Footer
st.write("### Stay healthy and enjoy your meals! 🌟")
