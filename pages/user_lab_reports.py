import streamlit as st
import sidebar
import fitz  # PyMuPDF
import re
import io
import numpy as np
import pickle
from PIL import Image

# Load model and tools
with open("model.pkl", "rb") as model_file:
    model = pickle.load(model_file)
with open("label_encoder.pkl", "rb") as le_file:
    label_encoder = pickle.load(le_file)
with open("scaler.pkl", "rb") as scaler_file:
    scaler = pickle.load(scaler_file)

# Sidebar and CSS
sidebar.render_sidebar()
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("userstyle.css")

# Text extraction from PDFs
def extract_text_from_pdf(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

# Convert image to PDF, then extract text using fitz
def extract_text_from_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PDF')
    img_pdf_bytes = img_byte_arr.getvalue()
    return extract_text_from_pdf(img_pdf_bytes)

# Regex extraction logic
TESTS = ["Blood Glucose", "HbA1C", "Systolic BP", "Diastolic BP", "LDL", "HDL", "Triglycerides", "Haemoglobin", "MCV"]
PATTERN = r"(?i)({})[^\d]+([\d]+(?:\.\d+)?)".format("|".join(TESTS))

def extract_medical_values(text):
    extracted = {}
    matches = re.findall(PATTERN, text)
    for key, value in matches:
        extracted[key.strip()] = float(value)
    return extracted

# Prediction logic
def predict_disease(values):
    EXPECTED = ["Blood Glucose", "HbA1C", "Systolic BP", "Diastolic BP", "LDL", "HDL", "Triglycerides", "Haemoglobin", "MCV"]
    features = [values.get(test, 0.0) for test in EXPECTED]
    features = np.array([features]).astype(float)
    scaled = scaler.transform(features)
    encoded = model.predict(scaled)[0]
    return label_encoder.inverse_transform([encoded])[0]

# Streamlit UI
st.subheader("🧪 Medical Test Results")

manual_values = {}
for test in TESTS:
    manual_values[test] = st.text_input(test)

st.markdown("### 📎 Upload Test Report (optional)")
uploaded_file = st.file_uploader("Upload PDF or Image (JPG, JPEG)", type=["pdf", "jpg", "jpeg"])

if st.button("Submit"):
    all_values = {}

    # Collect manual entries
    for k, v in manual_values.items():
        if v:
            try:
                all_values[k] = float(v)
            except:
                st.warning(f"Invalid number for {k}")

    # Extract from uploaded file
    if uploaded_file:
        file_bytes = uploaded_file.read()
        if uploaded_file.name.endswith(".pdf"):
            extracted_text = extract_text_from_pdf(file_bytes)
        else:
            extracted_text = extract_text_from_image(file_bytes)

        parsed_values = extract_medical_values(extracted_text)
        st.markdown("# 🔍 Extracted from file:")
        st.json(parsed_values)

        all_values.update(parsed_values)

    if all_values:
        prediction = predict_disease(all_values)
        st.success(f"🧬 Predicted Condition: **{prediction}**")
        medical_condition = prediction
        st.session_state.medical_conditions = medical_condition
    else:
        st.warning("Please enter test values manually or upload a valid report.")
