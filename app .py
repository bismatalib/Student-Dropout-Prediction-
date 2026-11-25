import json
import math
import streamlit as st

with open("model.json") as f:
    m = json.load(f)

def predict(info):
    row = dict(m["defaults"])
    row.update(info)
    z = m["intercept"]
    for col, w in zip(m["columns"], m["coef"]):
        x = row[col]
        if col in m["scaler"]:
            s = m["scaler"][col]
            x = (x - s["mean"]) / s["scale"]
        z += w * x
    return 1 / (1 + math.exp(-z))

def risk_level(p):
    if p < 0.30:
        return "Low Risk"
    elif p < 0.60:
        return "Medium Risk"
    return "High Risk"

st.title("Student Dropout Risk Predictor")
st.write("Enter the student's details to estimate dropout risk.")

age = st.slider("Age at enrollment", 17, 60, 20)
tuition = st.selectbox("Tuition fees up to date?", ["Yes", "No"])
debtor = st.selectbox("Debtor?", ["No", "Yes"])
scholar = st.selectbox("Scholarship holder?", ["No", "Yes"])
gender = st.selectbox("Gender", ["Female", "Male"])
a1 = st.slider("1st semester units approved", 0, 20, 5)
g1 = st.slider("1st semester grade", 0.0, 20.0, 12.0)
a2 = st.slider("2nd semester units approved", 0, 20, 5)
g2 = st.slider("2nd semester grade", 0.0, 20.0, 12.0)

if st.button("Predict"):
    info = {
        "Age at enrollment": age,
        "Tuition fees up to date": 1 if tuition == "Yes" else 0,
        "Debtor": 1 if debtor == "Yes" else 0,
        "Scholarship holder": 1 if scholar == "Yes" else 0,
        "Gender": 1 if gender == "Male" else 0,
        "Curricular units 1st sem (approved)": a1,
        "Curricular units 1st sem (grade)": g1,
        "Curricular units 2nd sem (approved)": a2,
        "Curricular units 2nd sem (grade)": g2,
    }
    p = predict(info)
    st.metric("Dropout probability", f"{p*100:.1f}%")
    level = risk_level(p)
    if level == "Low Risk":
        st.success(level)
    elif level == "Medium Risk":
        st.warning(level)
    else:
        st.error(level)
