import streamlit as st
import sidebar
import firebase_admin
from firebase_admin import credentials, firestore

db = firestore.client()

# === Sidebar and Style ===
sidebar.render_sidebar()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("userstyle.css")

# === Page Heading ===
st.subheader("Lifestyle")

# Option labels and corresponding numeric values
options = {
    "Never": 0,
    "Rarely": 1,
    "Occasionally": 2,
    "Frequently": 3,
    "Very Frequently": 4,
    "Always": 5
}

# === User Inputs ===
exercise_label = st.selectbox("Exercise", list(options.keys()))
smoking_label = st.selectbox("Smoking", list(options.keys()))
drinking_label = st.selectbox("Drinking", list(options.keys()))
job_hazard_label = st.selectbox("Job Hazard", list(options.keys()))
mental_stress_label = st.selectbox("Mental Stress", list(options.keys()))

if st.button("Submit"):
    # Convert labels to numeric values
    exercise = options[exercise_label]
    smoking = options[smoking_label]
    drinking = options[drinking_label]
    job_hazard = options[job_hazard_label]
    mental_stress = options[mental_stress_label]

    # Fetch all company lifestyle documents
    docs = db.collection("company_lifestyle").stream()

    # Initialize sum variables
    total_docs = 0
    sum_weights = {
        "exercise": 0,
        "smoking": 0,
        "drinking": 0,
        "job_hazard": 0,
        "mental_stress": 0
    }

    for doc in docs:
        data = doc.to_dict()
        total_docs += 1
        for key in sum_weights:
            sum_weights[key] += data.get(key, 0)

    if total_docs == 0:
        st.error("No company lifestyle data available.")
        st.stop()

    # Compute average weights (converted to proportion, summing to 1.0)
    avg_weights = {k: v / total_docs for k, v in sum_weights.items()}
    total_weight = sum(avg_weights.values())
    normalized_weights = {k: v / total_weight for k, v in avg_weights.items()}

    # Adjusted exercise (higher is better)
    adjusted_exercise = 5 - exercise

    # Compute health score using averaged weights
    weighted_sum = (
        adjusted_exercise * normalized_weights["exercise"] +
        smoking * normalized_weights["smoking"] +
        drinking * normalized_weights["drinking"] +
        job_hazard * normalized_weights["job_hazard"] +
        mental_stress * normalized_weights["mental_stress"]
    )

    health_score = max(0, min(5, weighted_sum))
    health_score = round(health_score, 2)
    st.info(f"Your calculated health score is: **{health_score:.2f} / 5**")
    st.session_state.health_score = health_score
