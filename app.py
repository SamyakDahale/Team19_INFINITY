import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

st.set_page_config(page_title="Login / Sign Up", layout="centered")


# Hide the Streamlit navigation (sidebar pages)
hide_nav_style = """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        [data-testid="stSidebarNav"] {
            display: none;
        }
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    </style>

"""
st.markdown(hide_nav_style, unsafe_allow_html=True)

# === Initialize Firebase App ===
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

# === Page Config ===
st.title("🔐 Welcome to Health Profile Portal")

if "view" not in st.session_state:
    st.session_state.view = "login"

# === View Switch Buttons ===
col1, col2 = st.columns(2)
with col1:
    if st.button("Login"):
        st.session_state.view = "login"
with col2:
    if st.button("Sign Up"):
        st.session_state.view = "signup"

st.markdown("---")

# === LOGIN FORM ===
if st.session_state.view == "login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Submit Login"):
        if username and password:
            user_ref = db.collection("USERS").document(username)
            user = user_ref.get()
            if user.exists:
                user_data = user.to_dict()
                if user_data["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_type = user_data.get("type", "Individual")

                    st.success(f"Welcome back, {username}! You are logged in as {st.session_state.user_type}.")

                    # Redirect / Conditional Rendering
                    if st.session_state.user_type == "Individual":
                        st.info("Redirecting to Individual Dashboard...")
                        st.switch_page("pages/individual_dashboard.py")  # You must have this page
                    elif st.session_state.user_type == "Company":
                        st.info("Redirecting to Company Dashboard...")
                        st.switch_page("pages/company_dashboard.py")  # You must have this page
                else:
                    st.error("Incorrect password.")
            else:
                st.error("User not found.")
        else:
            st.error("Please enter both username and password.")

# === SIGNUP FORM ===
elif st.session_state.view == "signup":
    st.subheader("Sign Up")
    new_username = st.text_input("Choose a Username")
    new_password = st.text_input("Choose a Password", type="password")
    email = st.text_input("Email Address")
    address = st.text_area("Address")
    contact = st.text_input("Contact Number")
    account_type = st.radio("Account Type", ["Individual", "Company"])

    if st.button("Create Account"):
        if all([new_username, new_password, email, address, contact]):
            user_ref = db.collection("USERS").document(new_username)
            if user_ref.get().exists:
                st.warning("Username already exists. Please choose another.")
            else:
                user_ref.set({
                    "username": new_username,
                    "password": new_password,  # Consider hashing in production!
                    "email": email,
                    "address": address,
                    "contact": contact,
                    "type": account_type
                })
                st.success(f"Account created for {new_username} as {account_type}!")
        else:
            st.error("Please fill in all the fields.")
