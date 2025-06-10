# 💡 InsureSmart

**Project by Team INFINITY**  
Presented at **INNOHACK 2025**, Chhatrapati Sambhajinagar’s biggest tech hackathon  
GitHub Repo: [INFINITY_Innohack](https://github.com/SamyakDahale/INFINITY_Innohack)

---

## 🔍 Problem Statement

**Title:** The Gap in Health Insurance Accessibility  
**Problem ID:** PS 15 (OPEN)

### 🚫 Issues Faced by Users:
- 🔒 Capital gets locked during manual policy processes
- ❌ Uncertain approval without health transparency
- 🔄 Lack of personalized suggestions
- 🚫 Limited ability to explore suitable plans

---

## ✅ Proposed Solution: **InsureSmart**

InsureSmart is an intelligent, data-driven web application that helps users:
- Upload medical reports (PDF/JPG)
- Get real-time health score analysis
- View insurance plans tailored to their health profile
- Suggest insurance plans using ML-based ranking
- Display company office location on a map

---

## 🏗️ System Architecture

- Upload medical reports → OCR parsing & preprocessing  
- Extract diagnostic values → Predict health score  
- Match user profile with plan database → Recommend top plans  
- Fetch company details → Display on interactive map

---

## 🧠 Technologies Used

| Layer | Technology |
|-------|------------|
| Frontend | Streamlit |
| Backend | Python |
| Database | Firebase |
| Document Parsing | Tesseract OCR, pdf2image, PIL |
| ML Model | Random Forest or MLP (`.pkl` format) |
| Dataset | [Diagnostic Pathology Test Results (Kaggle)](https://www.kaggle.com/datasets) |
| Deployment | Streamlit Cloud |
| Maps | Google Maps API (with fallback to OpenStreetMap) |

---

## 👥 Team INFINITY

| Name | Role |
|------|------|
| **Samyak Dahale** | Firebase Setup & Deployment |
| **Aditya Salunke** | ML Model Development & Integration |
| **Ganesh Kondke** | UI/UX Design & Frontend Support |
| **Attadeep Sawale** | Data Analysis & Streamlit App Development |

---

## 🚀 Live Demo

👉 **Deployed Project Link:** [[InsureSmart on Streamlit Cloud](https://insuresmart.streamlit.app/) ](https://infinityinnohack.streamlit.app/) 
*(Update the link if your actual Streamlit deployment URL is different)*

---
## 📝 How to Run Locally

    1. Clone the repo:
   ```bash
   git clone https://github.com/SamyakDahale/INFINITY_Innohack.git
   cd INFINITY_Innohack

   2. pip install -r requirements.txt
   3.streamlit run app.py


