import streamlit as st
from datetime import datetime, timedelta

#Files that we require#
bt = "bus_timings.txt"
bk = "booking.txt"
sd = "student_data.txt"

#Fuction for Authentication#
def validate_student(reg_no,dob):
    with open(sd,'r') as f:
        str = f.readlines
        reg = [line.strip().split(",") for line in str]
        for regi in reg:
            if regi[0]==reg_no and regi[1]==dob:
                return True
            else:
                return False

st.title("VTravel Booking Systum")
st.header("LOGIN")
reg_no = st.text_input("Enter Registration Number")
dob = st.text_input("Enter Date of Birth (DD-MM-YYYY)")
if st.button("Login"):
    if validate_student(reg_no,dob):
        st.success("Login Successful")
    else:
        st.error("Invalid Registration Number or Date of Birth")
        st.error("Outsider Detected")