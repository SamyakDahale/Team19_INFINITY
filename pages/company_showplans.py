import streamlit as st
import sidebar
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

# Sidebar
sidebar.render_sidebar()



db = firestore.client()

st.title("📋 Your Insurance Plans (Tabular View)")

# Check login
if "username" not in st.session_state or st.session_state.get("user_type") != "Company":
    st.warning("Please log in as a company to view your insurance plans.")
    st.stop()

company_username = st.session_state.username

# Fetch plans where 'company' matches username
plans_ref = db.collection("INSURANCE_PLANS").where("company_name", "==", company_username)
plans = plans_ref.stream()

# Collect data into list
plans_data = []
for plan in plans:
    data = plan.to_dict()
    plans_data.append({
        "Insurance Name": data.get("insurance_name", ""),
        "Premium (₹/10L)": data.get("premium", 0),
        "Min Health Score": data.get("min_health_score", 0),
        "Medical Condition": data.get("medical_condition", ""),
        "Pre-existing Diagnosis": data.get("existing_diagnosis", ""),
        "Add-ons": data.get("addons", ""),
        "Description": data.get("description", "")
    })

# Display in table
if plans_data:
    df = pd.DataFrame(plans_data)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No insurance plans found for your company.")
