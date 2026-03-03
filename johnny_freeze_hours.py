import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Excel file name
FILE_NAME = "JohnnyFreeze/johnny_freeze_hours.xlsx"

# Make sure file exists with correct columns
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Name", "Action", "Timestamp", "Elapsed"])
    df.to_excel(FILE_NAME, index=False)

def log_action(name, action):
    """Add a clock in/out entry to the Excel file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    df_existing = pd.read_excel(FILE_NAME)

    elapsed_time = ""

    if action == "Clock Out":
        # Find last clock-in for this user
        user_logs = df_existing[df_existing["Name"] == name]
        last_clock_in = user_logs[user_logs["Action"] == "Clock In"].tail(1)

        if len(last_clock_in) > 0:
            last_time = datetime.strptime(last_clock_in["Timestamp"].values[0], "%Y-%m-%d %H:%M:%S")
            now_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            delta = now_time - last_time
            elapsed_time = str(delta)
        else:
            elapsed_time = "No prior clock-in"

    new_entry = pd.DataFrame([[name, action, timestamp, elapsed_time]],
                             columns=["Name", "Action", "Timestamp", "Elapsed"])
    
    df_updated = pd.concat([df_existing, new_entry], ignore_index=True)
    df_updated.to_excel(FILE_NAME, index=False)


st.title("⏰ Clock In / Clock Out System")

name = st.text_input("Enter your name:")

col1, col2 = st.columns(2)

with col1:
    if st.button("Clock In"):
        if name.strip() == "":
            st.error("Please enter a name before clocking in.")
        else:
            log_action(name, "Clock In")
            st.success(f"{name} clocked in successfully!")

with col2:
    if st.button("Clock Out"):
        if name.strip() == "":
            st.error("Please enter a name before clocking out.")
        else:
            log_action(name, "Clock Out")
            st.success(f"{name} clocked out successfully!")

# Show logged data
if st.checkbox("Show recorded entries"):
    df_display = pd.read_excel(FILE_NAME)
    st.write(df_display)































