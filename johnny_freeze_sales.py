import streamlit as st
import pandas as pd
import os
from datetime import date

# Excel file path
excel_file = "/Users/jyoung/Documents/JohnnyFreeze/johnny_freeze_sales.xlsx"

# Page Navigation Functions
def go_to_page(page_name):
    st.session_state.page = page_name


# Flavor Page Function
def flavor_page(flavor_name):
    st.title(flavor_name)

    # Inputs
    current_date = date.today()
    selected_date = st.date_input("Date:", value=current_date)
    number = st.number_input(f"How many cups of {flavor_name} sold:", min_value=0, value=0)

    # Submit button
    if st.button("Submit Sales"):
        try:
            # Load existing data
            df = pd.read_excel(excel_file, index_col=0)
            df.index = pd.to_datetime(df.index).date  # convert to plain dates

            # Drop duplicate dates if they somehow exist (keep the first)
            df = df[~df.index.duplicated(keep="first")]

        except FileNotFoundError:
            # Create a new DataFrame if file doesn’t exist
            df = pd.DataFrame()

        # Ensure selected_date is a date object
        selected_date = selected_date if isinstance(selected_date, date) else selected_date.date()

        # Add column for this flavor if missing
        if flavor_name not in df.columns:
            df[flavor_name] = 0

        # Add new row for date if missing
        if selected_date not in df.index:
            df.loc[selected_date] = {col: 0 for col in df.columns}

        # Safely get the current value (convert NaN or missing to 0)
        current_value = df.loc[selected_date, flavor_name]
        if pd.isna(current_value):
            current_value = 0

        # Add the new number to existing total
        df.loc[selected_date, flavor_name] = current_value + number

        # Sort by date and save
        df.sort_index(inplace=True)
        df.to_excel(excel_file, index=True)

        st.success(f"✅ Saved {number} cups of {flavor_name} sold for {selected_date}!")

    # Back button
    if st.button("Back to Home"):
        go_to_page("home")


# Initialize Session State
if "page" not in st.session_state:
    st.session_state.page = "home"

# Flavor List
flavors = [
    "-",
    "Blue Raspberry",
    "Tiger Blood",
    "Banana",
    "Wedding Cake",
    "Strawberry Lemonade",
    "Sour Apple",
    "Cotton Candy",
    "Arctic Blast"
]

# Page Mapping
flavor_page_map = {
    "Blue Raspberry": "blue_razz",
    "Tiger Blood": "tiger_blood",
    "Banana": "banana",
    "Wedding Cake": "wedding_cake",
    "Strawberry Lemonade": "straw_lem",
    "Sour Apple": "sour_apple",
    "Cotton Candy": "cotton_candy",
    "Arctic Blast": "arctic_blast"
}


# -------------------------------
# Main App Logic
# -------------------------------

if st.session_state.page == "home":
    st.title("Johnny Freeze Sales Inputs")
    st.write("Select a flavor to enter its daily sales data.")

    selected_flavor = st.selectbox("Choose a flavor:", flavors)

    if selected_flavor != "-":
        if st.button(f"Go to {selected_flavor}"):
            page_id = flavor_page_map[selected_flavor]
            go_to_page(page_id)

# Render Flavor Pages Dynamically
elif st.session_state.page in flavor_page_map.values():
    current_flavor = next(
        key for key, value in flavor_page_map.items() if value == st.session_state.page
    )
    flavor_page(current_flavor)







