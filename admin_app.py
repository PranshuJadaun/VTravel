import streamlit as st
from datetime import datetime, timedelta
# Function to write updated bus timings
def save_bus_timings(bus_timings):
    with open(BUS_TIMINGS_FILE, "w") as f:
        for bus in bus_timings:
            f.write(f"{bus['route']},{bus['timing']},{bus['seats']}\n")

# Paths to data files
BUS_TIMINGS_FILE = "bus_timings.txt"
# Admin Panel
st.header("Admin Panel (For Bus Operators)")
with st.expander("Update Bus Timings"):
    route = st.selectbox("Select Route", ["Bus 1", "Bus 2"])
    new_time = st.time_input("New Timing")
    new_seats = st.number_input("Seats Available", min_value=0, step=1)
    
    if st.button("Update Timings"):
        for bus in bus_timings:
            if bus["route"] == route:
                bus["timing"] = new_time.strftime("%H:%M")
                bus["seats"] = new_seats
                save_bus_timings(bus_timings)
                st.success("Bus timings updated successfully")