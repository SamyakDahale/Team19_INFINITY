import streamlit as st
import sidebar
sidebar.render_sidebar()

# === Load External CSS ===
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("userstyle.css")

st.subheader("Eligible Sum Assured Value")

# Inputs
age = st.number_input("Age", min_value=0)
annual_income = st.number_input("Annual Income", min_value=0)
policy_value = st.number_input("Existing Policies' Value", min_value=0)

if st.button("Calculate Sum"):
    # Validation
    if age == 0 or annual_income == 0 or policy_value is None:
        st.error("Please fill in all required fields.")
    else:
        sum_assured = None
        if 20 <= age <= 30:
            sum_assured = (annual_income * 12) - policy_value
        elif 31 <= age <= 55:
            sum_assured = (annual_income * 7) - policy_value
        elif age > 55:
            sum_assured = (annual_income * 4) - policy_value
        else:
            st.error("Invalid age range. Must be 20 or above.")
        
        if sum_assured is not None:
            sum_assured = max(0, sum_assured)  # Ensure no negative values
            st.success(f"Eligible Sum Assured Value: ₹{sum_assured:,.2f}")
