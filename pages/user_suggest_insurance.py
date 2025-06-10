
import streamlit as st
import sidebar
sidebar.render_sidebar()
import firebase_admin
from firebase_admin import credentials, firestore
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

db = firestore.client()

# === Show stored health data ===
st.subheader("📋 Your Health Summary")

if "health_score" in st.session_state and "medical_conditions" in st.session_state and "existing_diagnosis" in st.session_state:
    health_score = st.session_state.health_score
    medical_conditions = st.session_state.medical_conditions
    existing_diagnosis = st.session_state.existing_diagnosis

    st.markdown(f"- **Health Score**: `{health_score}`")
    st.markdown(f"- **Medical Conditions**: `{(medical_conditions)}`")
    st.markdown(f"- **Existing Diagnoses**: `{(existing_diagnosis)}`")


    user_premium = st.number_input("Expected Premium", min_value=0)
    user_premium_type = st.radio("Premium Type wanted", ["Constant", "Floating"])
    user_addons = st.multiselect(
            "Select Add-ons",
            [
                "Critical Illness Cover",  "Maternity Cover", "Room Rent Waiver",  "Hospital Cash Benefit",
                "OPD Cover", "Accidental Death & Disability Cover", "International Coverage",
            ]
        )
else:
    st.warning("Health data not found in session.")
    st.stop()

# === Suggest Plan Button ===
if st.button("🎯 Suggest Suitable Plans"):
    plans_ref = db.collection("INSURANCE_PLANS").stream()

    plans = []
    similarities = []

    for doc in plans_ref:
        plan = doc.to_dict()
        plan_name = plan.get("insurance_name", "Unnamed Plan")
        # Extract plan data
        plan_health = plan.get("min_health_score", 0)
        plan_conditions = plan.get("medical_condition", [])
        plan_diagnosis = plan.get("existing_diagnosis", [])
        plan_premium = plan.get("premium", 0)
        plan_addons = plan.get("addons", [])
        plan_premium_type = plan.get("premium_type", "")

        # === Build Binary match features ===
        match_health = 1 if health_score >= plan_health else 0
        match_condition = 1 if plan_conditions in medical_conditions else 0
        match_diagnosis = 1 if plan_diagnosis in existing_diagnosis else 0
        match_premium = 1 if plan_premium <= user_premium else 0
        match_premium_type = 1 if plan_premium_type == user_premium_type else 0
        match_addon = 1 if any(add in plan_addons for add in user_addons) else 0

        # === Vector representations ===
        user_vector = np.array([1, 1, 1, 1, 1, 1])  # All inputs are equally weighted
        plan_vector = np.array([
            match_health,
            match_condition,
            match_diagnosis,
            match_premium,
            match_premium_type,
            match_addon
        ])

        similarity = cosine_similarity([user_vector], [plan_vector])[0][0]

        similarities.append((similarity, plan_name, plan))

    # Sort results by descending similarity
    similarities.sort(reverse=True, key=lambda x: x[0])

    # === Show Results ===
    if similarities:
        st.success("📑 Top 5 Plans Matched Based on Your Health Profile:")
        for sim, name, plan in similarities[:5]:
            st.markdown(f"### 🛡️ {name}")
            st.markdown(f"- **Match Score**: `{sim * 100:.2f}%`")
            st.markdown(f"- **Min Health Score**: `{plan.get('min_health_score')}`")
            st.markdown(f"- **Medical Conditions Covered**: `{plan.get('medical_condition', [])}`")
            st.markdown(f"- **Existing Diagnoses Covered**: `{plan.get('existing_diagnosis', [])}`")

            # === Fetch company details ===
            company_username = plan.get("company_name", None)  # ✅ Correct field name
            if company_username:
                user_query = db.collection("USERS").where("username", "==", company_username).stream()
                user_doc = next(user_query, None)
                if user_doc:
                    user_data = user_doc.to_dict()
                    st.markdown("**🏢 Company Information:**")
                    st.markdown(f"- **Company Name**: `{company_username}`")
                    st.markdown(f"- **Email**: `{user_data.get('email', 'N/A')}`")
                    st.markdown(f"- **Contact**: `{user_data.get('contact', 'N/A')}`")
                    st.markdown(f"- **Address**: `{user_data.get('address', 'N/A')}`")
                    csr = user_data.get('claim_settlement_ratio', None)
                    if csr is not None:
                        st.markdown(f"- **Claim Settlement Ratio**: `{float(csr) * 100:.2f}%`")
                    else:
                        st.markdown("- **Claim Settlement Ratio**: `N/A`")
                else:
                    st.markdown("**🏢 Company information not found in USERS collection.**")
            else:
                st.markdown("**🏢 Company name missing in plan data.**")

            st.markdown("---")
    else:
        st.info("No matching plans found.")

