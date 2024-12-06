import streamlit as st
from datetime import datetime, timedelta

# Paths to data files
BUS_TIMINGS_FILE = "./bus_timings.txt"
STUDENT_DATA_FILE = "./student_data.txt"
BOOKINGS_FILE = "./bookings.txt"

# Function to read bus timings
def load_bus_timings():
    with open(BUS_TIMINGS_FILE, "r") as f:
        lines = f.readlines()
    bus_timings = [line.strip().split(",") for line in lines]
    return [{"route": line[0], "timing": line[1], "seats": int(line[2])} for line in bus_timings]

# Function to write updated bus timings
def save_bus_timings(bus_timings):
    with open(BUS_TIMINGS_FILE, "w") as f:
        for bus in bus_timings:
            f.write(f"{bus['route']},{bus['timing']},{bus['seats']}\n")

# Function to validate student
def validate_student(reg_no, dob):
    with open(STUDENT_DATA_FILE, "r") as f:
        students = [line.strip().split(",") for line in f.readlines()]
    for student in students:
        if student[0] == reg_no and student[1] == dob:
            return True
    return False

# Function to check next bus timing
def get_next_bus(stop, bus_timings):
    now = datetime.now()
    for bus in bus_timings:
        bus_time = datetime.strptime(bus["timing"], "%H:%M")
        if bus_time >= now:
            return bus
    return None

# Function to book a seat
def book_seat(bus, reg_no):
    bus["seats"] -= 1
    with open(BOOKINGS_FILE, "a") as f:
        f.write(f"{reg_no},{bus['route']},{bus['timing']}\n")

# Main Streamlit app
st.title("VTravel Booking System")

# Load bus timings
bus_timings = load_bus_timings()

# Student login
st.header("Student Login")
reg_no = st.text_input("Enter Registration Number")
dob = st.text_input("Enter Date of Birth (YYYY-MM-DD)")

if st.button("Login"):
    if validate_student(reg_no, dob):
        st.success("Login Successful")
        
        # Select stop
        stop = st.selectbox("Select Your Stop", ["HOSTEL", "AB1", "AB2"])
        
        # Show next bus timing
        next_bus = get_next_bus(stop, bus_timings)
        if next_bus:
            st.info(f"Next Bus: {next_bus['route']} at {next_bus['timing']} (Seats Available: {next_bus['seats']})")
            
            # Booking option
            if next_bus["seats"] > 0:
                if st.button("Book Seat"):
                    book_seat(next_bus, reg_no)
                    save_bus_timings(bus_timings)
                    st.success("Seat Booked Successfully")
            else:
                st.error("No Seats Available")
        else:
            st.warning("No buses available at this time")
    else:
        st.error("Invalid Registration Number or Date of Birth")

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
