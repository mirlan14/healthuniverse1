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
    for column in ["Calories", "Total Fat (g)", "Protein (g)"]:
        selected_data[column] *= selected_data["Portions"]
    return selected_data, selected_data[["Calories", "Total Fat (g)", "Protein (g)"]].sum()

# Updated Bentley Dining Hall Data
dining_hall_data = {
    datetime(2023, 11, 13): {  # Monday
        "Breakfast": pd.DataFrame([
            {"Meal": "Bacon, Egg And Cheese Muffin", "Calories": 350, "Total Fat (g)": 12, "Protein (g)": 15},
            {"Meal": "Fried Egg O'muffin Sandwich", "Calories": 310, "Total Fat (g)": 10, "Protein (g)": 13},
            {"Meal": "Scrambled Eggs", "Calories": 190, "Total Fat (g)": 5, "Protein (g)": 12},
            {"Meal": "Bacon Slices", "Calories": 70, "Total Fat (g)": 6, "Protein (g)": 5},
            {"Meal": "Fried Tater Tots", "Calories": 250, "Total Fat (g)": 15, "Protein (g)": 2},
            {"Meal": "Buttermilk Pancakes", "Calories": 180, "Total Fat (g)": 9, "Protein (g)": 4},
        ]),
        "Lunch": pd.DataFrame([
            {"Meal": "Rosemary Grilled Pork Chop", "Calories": 300, "Total Fat (g)": 10, "Protein (g)": 30},
            {"Meal": "Grilled Fresh Tilapia", "Calories": 180, "Total Fat (g)": 5, "Protein (g)": 20},
            {"Meal": "Cheese Pizza", "Calories": 250, "Total Fat (g)": 8, "Protein (g)": 10},
            {"Meal": "Vegetable Lovers Feast Pizza", "Calories": 290, "Total Fat (g)": 12, "Protein (g)": 8},
        ]),
        "Dinner": pd.DataFrame([
            {"Meal": "Roast Loin Of Pork", "Calories": 210, "Total Fat (g)": 10, "Protein (g)": 25},
            {"Meal": "Rice & Red Beans", "Calories": 180, "Total Fat (g)": 3, "Protein (g)": 5},
            {"Meal": "Vegetable Lovers Feast Pizza", "Calories": 290, "Total Fat (g)": 12, "Protein (g)": 8},
        ]),
    },
    datetime(2023, 11, 14): {  # Tuesday
        "Breakfast": pd.DataFrame([
            {"Meal": "Scrambled Eggs", "Calories": 190, "Total Fat (g)": 5, "Protein (g)": 12},
            {"Meal": "Oatmeal", "Calories": 110, "Total Fat (g)": 1, "Protein (g)": 4},
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
}

# Sidebar for calendar selection
st.sidebar.header("Select Date and Meal Type")
selected_date = st.sidebar.date_input("Select a Date:", min_value=min(dining_hall_data.keys()), max_value=max(dining_hall_data.keys()))
selected_meal_type = st.sidebar.selectbox("Select a Meal Type:", ["Breakfast", "Lunch", "Dinner"])

# Retrieve menu for selected date and meal type
if selected_date in dining_hall_data:
    menu_df = dining_hall_data[selected_date][selected_meal_type]
else:
    st.error("No data available for the selected date.")
    st.stop()

# Display menu
st.subheader(f"{selected_date.strftime('%A, %B %d, %Y')} {selected_meal_type} Menu")
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
    if totals["Calories"] > daily_caloric_needs:
        st.error("Your meal plan exceeds your daily caloric needs.")
    elif totals["Calories"] < daily_caloric_needs * 0.8:
        st.warning("Your meal plan is too low in calories.")
    else:
        st.success("Your meal plan is within your recommended caloric range.")

# Footer
st.write("### Stay healthy and enjoy your meals! 🌟")
