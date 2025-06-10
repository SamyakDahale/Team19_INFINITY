import streamlit as st
import sidebar

st.set_page_config(
    page_title="Insurance Admin Dashboard",
    layout="wide",
)

sidebar.render_sidebar()


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("companystyle.css")


# ---------- Dashboard Title ----------
st.markdown('<div class="dashboard-title">Insurance Admin Dashboard</div>', unsafe_allow_html=True)

# ---------- Tab Buttons ----------
st.markdown("""
<div class="tab-buttons">
    <button class="tab-button active">Overview</button>
    <form action="/Insurances">
        <button class="tab-button" type="submit">Insurances</button>
    </form>
    <form action="/Add">
        <button class="tab-button" type="submit">Add</button>
    </form>
    <form action="/Lifestyle">
        <button class="tab-button" type="submit">Lifestyle</button>
    </form>
</div>
""", unsafe_allow_html=True)

# ---------- Info Cards ----------
st.markdown("""
<div class="card-container">
    <div class="card">
        <div class="card-icon">💲</div>
        <div class="card-label">Total Revenue</div>
        <div class="card-value">$1,235,000</div>
    </div>
    <div class="card">
        <div class="card-icon">👥</div>
        <div class="card-label">Total Customers</div>
        <div class="card-value">12,345</div>
    </div>
    <div class="card">
        <div class="card-icon">🛡️</div>
        <div class="card-label">Active Policies</div>
        <div class="card-value">8,765</div>
    </div>
</div>
""", unsafe_allow_html=True)